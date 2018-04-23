# Azure playbooks

## Provisioning

The current playbooks for Azure provisioning are under development.

### Where do I start?

Docs:
- http://docs.ansible.com/ansible/devel/scenario_guides/guide_azure.html
- https://docs.microsoft.com/en-us/azure/virtual-machines/linux/ansible-install-configure

Before any provisioning may occur, Azure account credentials must be present in the environment.  This can be accomplished by doing the following:

- Create the following file `~/.azure/credentials` with the contents:
   ```
   [myaccount]

   client_id = <client id>
   tenant = <tenant id>
   subscription_id = <subscription id>
   ```
   From the shell:
   ```
   $ export AZURE_PROFILE=myaccount
   ```

#### High-level overview
- prerequisites.yml - Provision resource group, storage account, vnet, and security groups.
- build_base_image.yml - Builds an up-to-date base image. 
- build_image.yml - Builds an Openshift node image.
- launch.yml - Creating a cluster happens through acs-engine.  A build of acs-engine and an openshift.json template is required.

The current expected work flow should be to provide base image (RHEL or CentOS) and then build a node image with access to Openshift repositories.  There should be a repository specified in the `openshift_additional_repos` parameter of the inventory file. The next expectation is a minimal set of values provided via an inventory file.

### Image publishing process

Once a node image has been created using managed disks, it then can be published in the market place.  The market place requires access to vhd blobs wherein it can copy these vhds and produce an image available in all zones.

The image publishing process requires the following steps:

Step 1:

- Create a node image

Step 2:

- run copy_md_to_vdh.yml
- At the current place in time the python cli for Azure does not generate valid sas URLs for the VHD files.  https://github.com/Azure/azure-cli/issues/6175
- This can be accomplished by:
  - logging into the UI
  - browse to the resource group
  - browse the storage account
  - select in the left bar (storage explorer preview)
  - select storage container
  - right click on the vhd object and 'Get shared access signature...'
  - the start date needs to preceed the current day 
  - the end date needs to be 3 weeks out
  - assign read/list permissions
  - click create
- Copy the created sas URLs from the previous step and place them into the inventory file used to publish the VM

Step 3:
