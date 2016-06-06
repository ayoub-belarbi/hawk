# -*- mode: ruby -*-
# vi: set ft=ruby :

def host_bind_address
  #DOCS: If the environment variable VAGRANT_INSECURE_FORWARDS is set to "yes, y, true or on" then it will expose all the ip addresses in the guest machine to the host machine from port 3000 of the guest machine to the port 3000 of the host machine and vice versa
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
    #DOCS: Chef solo expect that the cookbooks and recipes exists in the same system that will be running on (vagrant nodes), it exists in the chef directory and synchronized with rsync
    #DOCS: The default recipe is default.rb, other recipes are variation of this.
    #DOCS: This will tell vagrant to launch vagrant and specify the chef/cookbooks directory as the cookbook path, normally this is done by specifying this in solo.rb but instead of that, this is done by vagrant:
    chef.cookbooks_path = ["chef/cookbooks"]
    #DOCS: Contain the run list configurations, in our case this is not done by a json file but a ruby file like roles/base.rb
    chef.roles_path = ["chef/roles"]
     #DOCS: This will launch chef-solo -c solo.rb
    chef.custom_config_path = "chef/solo.rb"
    #DOCS: chef.synced_folder_type = "rsync" # Why we need rsync when we have vagrant synchronization
    chef.synced_folder_type = "rsync"
    roles.each do |role|
      chef.add_role role
    end
  end
  #DOCS: Config for the virtual machines, the first one is the one that vagrant will try to use as default one
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
  #DOCS: Global so it affects all the nodes, A standard openSUSE Leap 42.1 x86_64 box, including Chef(solo), Puppet and Bindfs for Virtualbox, VMWare and libvirt
  config.vm.box = "opensuse/openSUSE-42.1-x86_64"
  config.vm.box_check_update = true
  #DOCS: No need to ssh insert key because we don't have concerns about security here and maybe this option make some troubles
  config.ssh.insert_key = false
  #DOCS: All this section is about performance issue for using essentially virtualbox, to overcome that, we use nfs combined with bindfs
  #DOCS: Nfs is better in performance that's why we used.
  config.vm.synced_folder ".", "/vagrant", type: "nfs", mount_options: ["rw", "noatime", "async"]
  config.bindfs.bind_folder "/vagrant", "/vagrant", force_user: "hacluster", force_group: "haclient", perms: "u=rwX:g=rwXD:o=rXD", after: :provision
  #DOCS: When using nfs, files has problem with permissions (An NFS mount has the same numeric permissions in the guest as in the host)
  #DOCS: Simply to solve this probem:
  #DOCS: 1- mount your share over NFS into a temporary location in the guest
  #DOCS: 2- re-mount the share to the actual destination with vagrant-bindfs, setting the correct permissions
  config.vm.define "webui", primary: true do |machine|
    machine.vm.hostname = "webui"
    machine.vm.network :forwarded_port, host_ip: host_bind_address, guest: 3000, host: 3000
    configure_machine machine, 0, ["base", "webui"], 1024
  end

  1.upto(2).each do |i|
    #DOCS: autostart: false to prevent the node machines for starting when vagrant up
    config.vm.define "node#{i}", autostart: true do |machine|
      machine.vm.hostname = "node#{i}"
      configure_machine machine, i, ["base", "node"], 512
    end
  end
  #DOCS: In case of any provider above didn't work, use libvirt
  config.vm.provider :libvirt do |provider, override|
    provider.storage_pool_name = "default"
    provider.management_network_name = "vagrant"
  end
end
