# isp-programmer
ISP Programmer for NXP Cortex-M Chips

Command-line tool for programming NXP microcontrollers via the UART ISP interface.

## Features
### Secure Write

To prevent bricking the chip during an interrupted write:

- The checksum in flash is first set to zero, forcing the chip to boot into ISP mode if power is lost.
- The image is then written from the topmost page down to the first page.
- The first sector (which contains the valid checksum) is written last.

This ensures that any failure during programming will leave the chip in ISP mode.

### Auto ISP Mode Entry
The `--isp-entry` option controls the UART RTS and DTR lines to automatically enter ISP mode. This option requires:
- DTR connects to chip /Reset pin
- RTS connects to chip ISP_Entry pin

Alternatively, you can manually enter ISP mode by asserting both /Reset and ISP_Entry pins low, then releasing /Reset.

## Chip Families Supported:
+ LPC80x
    + LPC802
    + LPC804
+ LPC82x
    + LPC822
    + LPC824
+ LPC84x
    + LPC844
    + LPC845

### Untested, expected to work
+ LPC81x
    + LPC810
    + LPC811
    + LPC812
+ LPC83x
    + LPC832
    + LPC834
+ LPC86x
    + LPC865

Chips using UU-encoded protocols (e.g., LPC1700 family) are not supported.
Other NXP devices with 1 kB sectors *may* work if added to the `lpctools_parts.def` file.

The configuration file is identical to that used by the [lpctools project](http://git.techno-innov.fr/?p=lpctools).

## Installation

### From PyPI

```bash
pipx install ispprogrammer
```

### From Source
```bash
git clone https://github.com/snhobbs/isp-programmer.git
cd isp-programmer
pipx install . --force
```

> Default chip definitions are bundled. For custom chips, use the --config-file flag or copy your lpctools_parts.def to /etc/lpctools_parts.def.


## Usage
### Erase Entire Flash with Auto ISP Mode Entry
```bash
ispprogrammer --device /dev/ttyUSB0 --isp-entry erase
```

### Program Flash Image
```bash
ispprogrammer --device /dev/ttyUSB0 -b 9600 -crystal_frequency 12000 writeimage --imagein blinky804.hex
```

### Read Chip Info
```bash
ispprogrammer --device /dev/ttyUSB0 -b 9600 -crystal_frequency 12000 querychip
```

## Similar Projects
+ [MXLI by JitterCompany](https://github.com/JitterCompany/mxli)
+ [NXP ISP by idreamoferp](https://github.com/idreamoferp/nxp_isp)
+ [NXP ISP Loader by pzn1977](https://github.com/pzn1977/nxp_isp_loader)
+ [LPC81x ISP Tool by laneboysrc](https://github.com/laneboysrc/LPC81x-ISP-tool)
+ [LPC21ISP by Senseg](https://github.com/Senseg/lpc21isp)
+ [Nxpprog by ulfen](https://github.com/ulfen/nxpprog)
