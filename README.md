# gpydem

GPy modem - 3G GSM USB modem handler.

Handling USB GSM devices under Linux via AT commands.

## Features

* set up device
* set PIN code to unlock SIM card
* read/delete received SMS messages
* send SMS messages

## Installation

### libs

Install extra libraries that this package depends on:
``` sh
opkg install python-light python-setuptools python-pyserial
#pip install python-serial
```

### pip

Install this package via **pip** package manager:
``` sh
pip install gpydem
```

### setup.py

Install this package manually via **setup.py** file:
``` sh
git clone https://github.com/kyuzom/gpydem
cd gpydem
python setup.py install
```

## Prepare USB device mount

### udev rule

**NOTE!** Additional files can be found under the [rules.d](system/etc/udev/rules.d) directory.

Collect information about your USB modem:
``` sh
udevadm info -a /dev/ttyUSB0
```

Look for unique attributes like: **ATTRS{idProduct}**, **ATTRS{idVendor}**

Put your udev rules into the */etc/udev/rules.d* folder, then reload your udev rules:
``` sh
udevadm control --reload
```

Activate your rules in this way if you prefer to leave your device plugged in:
``` sh
udevadm trigger
```

Check your tty USB devices:
``` sh
ls -l /dev/ttyUSB*
```

## Usage

### cmd line

Test functionality via reading SMS messages:
``` sh
python /path/to/extras/gpydemsms.py -r -i /dev/ttyUSBalarmE220
```

### python lib

Use as an external library:
``` python
from __future__ import print_function
import gpydem
gsm = gpydem.Modem.get("HuaweiE220", "/dev/ttyUSBalarmE220", baudrate=9600)
for msg in gsm.messages():
    print("UnRead message #%d: %s" % (msg.index, msg.text))
```

## License

gpydem is MIT licensed. See the included [LICENSE](LICENSE) file.
