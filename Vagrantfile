# -*- mode: ruby -*-
# vi: set ft=ruby :

# Note: vagrant plugin install vagrant-triggers

require 'yaml'
require 'base64'
require 'tempfile'
require 'json'

#
# Basic configuration
#

version = File.read('VERSION')

global_config = YAML.load_file('deploy.yml')

app_config = global_config['app']

appdata_config = global_config['app_data']

#
# Globals
#

server_name = app_config.fetch('server_name', 'helloworld.internal')

address = app_config.fetch('address', '127.0.0.1')

scheme = app_config.fetch('https')? 'https' : 'http'

#
# Helpers
#

def j2(infile, outfile, **context)
  # Note: Needs j2 command (pip install j2cli)
  t = Tempfile.new(['helloworld', '.json'])
  File.write(t.path, JSON.dump(context))
  File.write(outfile, run("j2 #{infile} #{t.path}"))
end

def run_docker_build(image_name, dockerfile: 'Dockerfile', build_args: {})
  extra_args = build_args.map do |k, v| "--build-arg #{k}=#{v}" end
  run "docker build -t #{image_name} -f #{dockerfile} #{extra_args.join(' ')} ."
end

def to_command_args(**kwargs)
    # Transform keyword args to an array of getopt-style command args
    r = kwargs.map do |k, v| 
      k = k.to_s().gsub('_', '-')
      if v.instance_of?(Array)
        v.map do |v1| "--#{k}=#{v1}" end
      else 
        "--#{k}=#{v}"
      end
    end
    r.flatten()
end

#
# Vagrant directives
#

Vagrant.configure(2) do |config|
    
  ## Prepare source distribution
  
  config.trigger.before :up, :vm => '^app$' do
    run "python setup.py sdist"
  end 
  
  ## Prepare needed Docker images

  config.trigger.before :up, :vm => '^app-data$' do
    run_docker_build "local/helloworld-data:#{version}",
      dockerfile: "deploy/app-data/Dockerfile"
  end
  
  config.trigger.before :up, :vm => '^app$' do
    run_docker_build "local/httpd:2.4-mod_wsgi",
      dockerfile: "deploy/httpd/Dockerfile"
  end

  config.trigger.before :up, :vm => '^app$' do
    if scheme == 'https'
      vhost_tpl_name = 'vhost-ssl.conf.j2'
      dockerfile = 'vhost-ssl.dockerfile'
    else
      vhost_tpl_name = 'vhost.conf.j2'
      dockerfile = 'vhost.dockerfile'
    end
    j2 "deploy/app/config.ini.j2", "deploy/app/config.ini",
      :session_secret => Base64.encode64(Random.new.bytes(16)).strip(),
      :session_timeout => 7200
    j2 "deploy/app/#{vhost_tpl_name}", "deploy/app/vhost.conf",
      :name => app_config['name'],
      :num_processes => app_config['wsgi']['num_processes'],
      :num_threads => app_config['wsgi']['num_threads']
    run_docker_build "local/helloworld:#{version}",
      :dockerfile => "deploy/app/#{dockerfile}",
      :build_args => {:version => version}
  end

  ## Create data volume container (helloworld-data) 

  config.vm.define "app-data" do |container|
    container.vm.provider "docker" do |p|
      p.image = "local/helloworld-data:#{version}"
      p.name = "helloworld-data"
      p.create_args = to_command_args(
        :hostname => "helloworld-data.internal")
      p.remains_running = false
    end
    container.vm.synced_folder ".", "/vagrant", disabled: true
  end

  ## Create application container (helloworld) 
  
  config.vm.define "app" do |container|
    container.vm.provider "docker" do |p|
      p.image = "local/helloworld:#{version}"
      p.name = "helloworld"
      p.env = {
         'SERVER_NAME' => server_name
      }
      p.create_args = to_command_args(
        :hostname => "helloworld.internal",
        :volumes_from => "helloworld-data",
        :publish => ["#{address}:80:80", "#{address}:443:443"])
    end
    container.vm.synced_folder ".", "/vagrant", disabled: true
  end

end
