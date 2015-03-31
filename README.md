# Crowsnest

Crowsnest is a research SDN application developed at Lancaster Unviersity.
Crowsnest facillitates the collection of QoE metrics for Video on
Demand content in OpenFlow enabled networks.

Crowsnest is built with Python and targets version 2.7. It has only been tested
in Unix environments, and no promises are made for its stability. It is very
much a work in progress.


### Installation

2 tools are necessary to run crowsnest: Python 2.7 and MongoDB v2.x.

Everything else should be handled by running the following from the root of the
project directory:

`pip install -r requirements.txt`

Some installations of Python 2.7 do not ship with `pip` by default, so if
`which pip` doesn't return a result, visit the Python project homepage for
instructions on how to install `pip`.

### Run

Crowsnest can be started with its default configuration, or it can be ran with a
user specified configuration file in situations where port mappings overlap
with other services on a machine. 

_Basic_

`./start`

_With Configuration_

`./start --config examples/config/node.yaml`

`./start -h` to see all available options


### Usage

To collect metrics, traffic must be sent to the machine running crowsnest by
whatever means you desire. We include a simple packet duplication rule to be
installed on an OF switch in the `examples/sdn/` directory. If you read
`TESTING.md`, we provide a walkthrough of how we use this SDN rule.

Once crowsnest is running and receiving packets, you can retrieve and observe
the data through the GUI or the API.

By default, the GUI binds to 0.0.0.0:80, and provides graphical access to all
ongoing and completed sessions.

The API, by default, binds to 0.0.0.0:5000. Using the interface as detailed in
`API.md`, it is possible to retrieve data as it is stored on the local machine
as JSON.