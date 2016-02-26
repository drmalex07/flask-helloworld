# -*- mode: ruby -*-
# vi: set ft=ruby :

# Note: vagrant plugin install vagrant-triggers

require 'yaml'
require 'base64'
require 'tempfile'
require 'json'

#
# Environment
#

ENV['VAGRANT_DEFAULT_PROVIDER'] = 'docker'
ENV['VAGRANT_NO_PARALLEL'] = 'yes'

#
# Basic configuration
#

version = File.read('VERSION')

global_config = YAML.load_file('deploy.yml')

app_config = global_config['containers']['app']

database_config = global_config['containers']['database']

#
# Globals
#

server_name = app_config.fetch('server_name', 'helloworld.internal')

address = app_config.fetch('address', '127.0.0.1')

forwarded_ports = app_config.fetch('forwarded_ports', ['80:80']).map do |u| u.split(':') end

scheme = app_config.fetch('https')? 'https' : 'http'

db_file = database_config['file']

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
  return
end

def to_command_args(**kwargs)
    # Transform keyword args to an array of getopt-style command args
    a = lambda do |k, v| "--#{k}=#{v}" end
    r = kwargs.map do |k, v| 
      k = k.to_s().gsub('_', '-')
      if v.instance_of?(Array)
        v.map do |v1| a.call(k, v1) end
      else 
        a.call(k, v)
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

  config.trigger.before :up, :vm => '^database$' do
    if (db_file and File.exists?(db_file))
      run_docker_build "local/helloworld-database:#{version}",
        dockerfile: "deploy/database/database.dockerfile",
        build_args: {:db_file => db_file}
    else
      run_docker_build "local/helloworld-database:#{version}",
        dockerfile: "deploy/database/database-empty.dockerfile"
    end
  end
  
  config.trigger.before :up, :vm => '^app$' do
    run_docker_build "local/httpd:2.4-mod_wsgi",
      dockerfile: "deploy/httpd/Dockerfile"
  end

  config.trigger.before :up, :vm => '^app$' do
    vhost_vars = {
      :name => app_config['name'],
      :num_processes => app_config['wsgi']['num_processes'],
      :num_threads => app_config['wsgi']['num_threads']
    }
    j2 "deploy/app/config.ini.j2", "deploy/app/config.ini",
      :session_secret => Base64.encode64(Random.new.bytes(16)).strip(),
      :session_timeout => 7200
    if scheme == 'https'
      j2 "deploy/app/vhost-ssl.conf.j2", "deploy/app/vhost.conf", **vhost_vars
      run_docker_build "local/helloworld:#{version}",
        :dockerfile => "deploy/app/vhost-ssl.dockerfile",
        :build_args => {:version => version}
    else
      j2 "deploy/app/vhost.conf.j2", "deploy/app/vhost.conf", **vhost_vars
      run_docker_build "local/helloworld:#{version}",
        :dockerfile => "deploy/app/vhost.dockerfile",
        :build_args => {:version => version}
    end
  end

  ## Display info

  config.trigger.after :up, :vm => '^app$' do
    info "The application is started; Browse #{scheme}://#{server_name}"
  end

  ## Create data volume container (helloworld-database) 

  config.vm.define "database" do |container|
    container.vm.provider "docker" do |p|
      p.image = "local/helloworld-database:#{version}"
      p.name = "helloworld-database"
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
      p.ports = forwarded_ports.map do |host_port, port| "#{address}:#{host_port}:#{port}" end
      p.create_args = to_command_args(
        :volumes_from => "helloworld-database",
      )
    end
    container.vm.synced_folder ".", "/vagrant", disabled: true
  end

end
