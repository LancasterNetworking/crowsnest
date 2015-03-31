# Testing

## Starting the test environment

We provide a vagrant image for testing. If you want to do your own testing, you'll need Vagrant too. [Get it here](https://www.vagrantup.com)

### Step 1

Fetch and initialise the VM image using:

`$ vagrant up`


### Step 2

You'll need two shell sessions for testing, start them with:

`$ vagrant ssh`

### Step 3

We need an OpenFlow controller. Any will do, but we ship our image with Floodlight preinstalled. Start Floodlight in one of the two shell sessions:

`$ java -jar ~/floodlight/target/floodlight.jar`

### Step 4

We provision virtualised hosts using Mininet, which comes preinstalled in our image. Start mininet in the second shell session like so:

`$ sudo python /vagrant/examples/topology/simple.py`

### Step 5

The previous step provisions 4 hosts and leaves you in the mininet shell, `mininet>`. To interact with the hosts efficiently, you'll need an implementation of the X Windowing System. If you're on Linux, see `xorg`; OS X, see `XQuartz`. Open shell sessions for each host with xterm:

`mininet> xterm h1 h2 h3 h4`

Start serving content on host 2 (h2) by running:

`$ cd /srv && python -m SimpleHTTPServer 80`

Start crowsnest on host 3 (h3) by running:

`$ python /vagrant/start --config /vagrant/examples/config/node.yaml`

Using host 4 (h4) we duplicate and redirect traffic destined for h2 to h3:

`$ python /vagrant/examples/sdn/rules.py`

Start scootplayer to begin video playback

`$ python /home/vagrant/scootplayer/scootplayer.py -m http://10.0.0.2/bunny_2s/BigBuckBunny_2s_isoffmain_DIS_23009_1_v_2_1c2_2011_08_30.mpd`