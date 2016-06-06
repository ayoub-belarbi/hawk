# -*- mode: ruby -*-
# vi: set ft=ruby :

def host_bind_address
  #If the env var VAGRANT_INSECURE_FORWARDS is set to "yes, y, true, on" then expose all the ip address in the guest machine to the host machine from port 22 to the port 3000
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
    # Chef solo expect that the cookbooks and recepies exists in the same system that will be runing on (vagrant nodes), that exist in the chef dir and syncronized with rsync
    # the default recipe is default.rb, other recipes are variation of this.
    # this will tell vagrant to launch vagrant and specify the chef/cookbooks dir as the cookbook path, normally this is done by specifying this in solo.rb but instead, this is done by vagrant:
    chef.cookbooks_path = ["chef/cookbooks"]
    # Contain the run list configurations, in our case this is not done by a json file but a ruby file like roles/base.rb
    chef.roles_path = ["chef/roles"]
     # this will launch chef-solo -c solo.rb
    chef.custom_config_path = "chef/solo.rb"
    # chef.synced_folder_type = "rsync" # Why we need rsync when we have vagrant
    chef.synced_folder_type = "rsync"
    roles.each do |role|
      chef.add_role role
    end
  end
  # Config for the virt machines, the first one is the one that vagrant will try to use as default one
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
  # Global so it affects all the nodes, A standard openSUSE Leap 42.1 x86_64 box, including Chef(solo), Puppet and Bindfs for Virtualbox, VMWare and libvirt
  config.vm.box = "opensuse/openSUSE-42.1-x86_64"
  config.vm.box_check_update = true
  # No need to ssh insert key because we dont have concerns about security here and maybe this option make some troubles | # Global so it affects all the nodes
  config.ssh.insert_key = false
  # All this section is about performance issue for using essentially virtualbox, to overcome that, we use nfs combined with bindfs
  # Nfs is better in performance that's why we used. check with Kris
  config.vm.synced_folder ".", "/vagrant", type: "nfs", mount_options: ["rw", "noatime", "async"]
  config.bindfs.bind_folder "/vagrant", "/vagrant", force_user: "hacluster", force_group: "haclient", perms: "u=rwX:g=rwXD:o=rXD", after: :provision
  # When using nfs, files has problem with permissions (An NFS mount has the same numeric permissions in the guest as in the host)
  # Simply to solve this probem :
  # mount your share over NFS into a temporary location in the guest
  # re-mount the share to the actual destination with vagrant-bindfs, setting the correct permissions
  config.vm.define "webui", primary: true do |machine|
    machine.vm.hostname = "webui"
    machine.vm.network :forwarded_port, host_ip: host_bind_address, guest: 3000, host: 3000
    configure_machine machine, 0, ["base", "webui"], 1024
  end

  1.upto(2).each do |i|
    #autostart: false to prevent the node machines for starting when vagrant up
    config.vm.define "node#{i}", autostart: true do |machine|
      machine.vm.hostname = "node#{i}"
      configure_machine machine, i, ["base", "node"], 512
    end
  end
  # In case of any provider above didn't work, use libvirt
  config.vm.provider :libvirt do |provider, override|
    provider.storage_pool_name = "default"
    provider.management_network_name = "vagrant"
  end
end
