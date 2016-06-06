# -*- mode: ruby -*-
# vi: set ft=ruby :

def host_bind_address
  ENV['VAGRANT_INSECURE_FORWARDS'] =~ /^(y(es)?|true|on)$/i ? '*' : '127.0.0.1'
end

$shared_disk = '.vagrant/_shared_disk'
$shared_disk_size = 128 # MB

# Create and attach shared SBD/OCFS2 disk for VirtualBox
class VagrantPlugins::ProviderVirtualBox::Action::SetName
  alias_method :original_call, :call
  def call(env)
    disk_file = "#{$shared_disk}.vdi"
    ui = env[:ui]
    driver = env[:machine].provider.driver
    uuid = driver.instance_eval { @uuid }
    if !File.exist?(disk_file)
      ui.info "Creating storage file '#{disk_file}'..."
      driver.execute('createhd', "--filename", disk_file, "--size", "#{$shared_disk_size}", '--variant', 'fixed')
      driver.execute('modifyhd', disk_file, '--type', 'shareable')
    end
    ui.info "Attaching '#{disk_file}'..."
    driver.execute('storageattach', uuid, '--storagectl', "SATA Controller", '--port', "1", '--device', "0", '--type', 'hdd', '--medium', disk_file)
    original_call(env)
  end
end

# Shared configuration for all VMs
def configure_machine(machine, idx, roles, memory)
  machine.vm.network :forwarded_port, host_ip: host_bind_address, guest: 22, host: 3022 + (idx * 100)
  machine.vm.network :forwarded_port, host_ip: host_bind_address, guest: 7630, host: 7630 + idx
  machine.vm.network :private_network, ip: "10.13.37.#{10 + idx}"

  machine.vm.provision "shell", path: "chef/suse-prepare.sh"
  machine.vm.provision :chef_solo do |chef|
    chef.cookbooks_path = ["chef/cookbooks"]
    chef.roles_path = ["chef/roles"]
    chef.custom_config_path = "chef/solo.rb"
    chef.synced_folder_type = "rsync"
    roles.each do |role|
      chef.add_role role
    end
  end

  machine.vm.provider :virtualbox do |provider, override|
    provider.memory = memory
    provider.cpus = 1
    provider.name = "hawk-#{machine.vm.hostname}"
  end

  machine.vm.provider :libvirt do |provider, override|
    provider.memory = memory
    provider.cpus = 1
    provider.graphics_port = 9200 + idx
    provider.storage :file, path: "#{$shared_disk}.raw", size: "#{$shared_disk_size}M", type: 'raw', :bus=> 'scsi', :device=>'sdb', cache: 'none', allow_existing: true

  end
end

Vagrant.configure("2") do |config|
  unless Vagrant.has_plugin?("vagrant-bindfs")
    abort 'Missing bindfs plugin! Please install using vagrant plugin install vagrant-bindfs'
  end

  config.vm.box = "opensuse/openSUSE-42.1-x86_64"
  config.vm.box_check_update = true
  config.ssh.insert_key = false
  config.vm.synced_folder ".", "/vagrant", type: "nfs", mount_options: ["rw", "noatime", "async"]
  config.bindfs.bind_folder "/vagrant", "/vagrant", force_user: "hacluster", force_group: "haclient", perms: "u=rwX:g=rwXD:o=rXD", after: :provision



#################DOCS:   Configuration for the primary node############################
  config.vm.define "webui", primary: true do |machine|
    machine.vm.hostname = "webui"
    machine.vm.network :forwarded_port, host_ip: host_bind_address, guest: 3000, host: 3000
    configure_machine machine, 0, ["base", "webui"], 1024


  end
############################DOCS:  End configuration first machine#####################

  1.upto(2).each do |i|
    config.vm.define "node#{i}", autostart: true do |machine|

      machine.vm.hostname = "node#{i}"
      configure_machine machine, i, ["base", "node"], 512


    end
  end
############## DOCS:  END Configuration for the 3 other nodes node#####################

  # DOCS:  In case of any provider above didn't work, use libvirt
  config.vm.provider :libvirt do |provider, override|
    provider.storage_pool_name = "default"
    provider.management_network_name = "vagrant"
  end

end
