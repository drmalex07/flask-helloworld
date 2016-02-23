# -*- mode: ruby -*-
# vi: set ft=ruby :

# Note: vagrant plugin install vagrant-triggers

require 'base64'
require 'tempfile'
require 'json'

VERSION = File.read('VERSION')

SERVER_NAME = 'helloworld.internal'

SERVER_ADDRESS = '127.0.100.3' 

public_address = SERVER_ADDRESS

#
# Helpers
#

def generate_file(path, tpl_path, context: {})
  # Note: Needs j2 command (pip install j2cli)
  t = Tempfile.new(['helloworld', '.json'])
  File.write(t.path, JSON.dump(context))
  File.write(path, run("j2 #{tpl_path} #{t.path}"))
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
    run_docker_build "local/helloworld-data:#{VERSION}",
      dockerfile: "deploy/app-data/Dockerfile"
  end
  
  config.trigger.before :up, :vm => '^app$' do
    run_docker_build "local/httpd:2.4-mod_wsgi",
      dockerfile: "deploy/httpd/Dockerfile"
  end

  config.trigger.before :up, :vm => '^app$' do
    context = {
      :session_secret => Base64.encode64(Random.new.bytes(16)).strip(),
      :session_timeout => 7200, 
    }
    generate_file "deploy/app/config.ini", "deploy/app/config.ini.j2",
      context: context
    run_docker_build "local/helloworld:#{VERSION}",
      dockerfile: 'deploy/app/Dockerfile',
      build_args: {:version => VERSION}
  end

  ## Create data volume container (helloworld-data) 

  config.vm.define "app-data" do |container|
    container.vm.provider "docker" do |p|
      p.image = "local/helloworld-data:#{VERSION}"
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
      p.image = "local/helloworld:#{VERSION}"
      p.name = "helloworld"
      p.env = {
         'SERVER_NAME' => SERVER_NAME
      }
      p.create_args = to_command_args(
        :hostname => "helloworld.internal",
        :volumes_from => "helloworld-data",
        :publish => ["#{public_address}:80:80", "#{public_address}:443:443"])
    end
    container.vm.synced_folder ".", "/vagrant", disabled: true
  end

end
