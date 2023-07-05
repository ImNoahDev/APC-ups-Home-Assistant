# APC ups Home Assistant
This allows you to broadcast your APC UPS information and status from the computer it is connected to, to home assistant

## Usage

### All operating systems
This assumes that [**apcupsd**](http://www.apcupsd.org) has already been installed:

Dowload the [Universal release](https://github.com/dev-bash/APC-ups-Home-Assistant/releases/download/Release/Universal.zip) of this script and install [**TMUX**](https://github.com/tmux/tmux/wiki), edit the ApcStartup.sh file and put the path of the python script in (apc.py).

Go co cronjob with ```crontab -e```, press ```i``` then add ```@reboot /path/to/script/ApcStartup.sh``` (make sure to put the correct path to ApcStartup.sh), then press ```esc``` and type ```:wq``` to save

reboot your system and check the output of ```http://<Server IP>:5000/apcaccess```

### Unraid
If you are on unraid:
Download the USER SCRIPTS, PYTHON3 and [UNRAID-TMUX](https://gist.githubusercontent.com/justin-himself/2ce4af30dd9fc372df7aadb64fd4df35/raw/0a66faaa79670d1946ba3c8b1643f844406b7938/unraid-tmux.plg) plugins then download the [unraid release](https://github.com/dev-bash/APC-ups-Home-Assistant/releases/download/Release/Unraid.zip) of this project


Place the **APC UPS** folder in the **/boot/config/plugins/user.scripts/scripts/** directory

Go to Settings > User Scripts and set the **APC UPS** script to run **At startup of array** (If the script does not appear, try restarting unraid first)

Restart unraid or the array to make the script run and verify it has started succesfully by going to ```http://<Unraid IP>:5000/apcaccess``` and checking the output

## Home Assistant
Go to Configuration.yaml and place this inside:
**Be sure to change ```<Server ip>``` to the ip of the server/computer that has the ups connected**

```
sensor:
  - platform: rest
    resource: http://<Server ip>:5000/apcaccess
    name: ups
    value_template: "{{ value_json.output }}"
    json_attributes:
      - STATUS
      - BCHARGE
      - TIMELEFT
      - BATTV
      - NOMBATTV
    scan_interval: 10

  - platform: template
    sensors:
      ups_status:
        friendly_name: UPS Status
        value_template: "{{ state_attr('sensor.ups', 'STATUS') }}"
      ups_battery_charge:
        friendly_name: UPS Battery Charge
        value_template: "{{ state_attr('sensor.ups', 'BCHARGE') | regex_replace('[^0-9.]','') | float }}"
        unit_of_measurement: "%"
      ups_battery_voltage:
        friendly_name: UPS Battery Voltage
        value_template: "{{ state_attr('sensor.ups', 'BATTV') | regex_replace('[^0-9.]','') | float }}"
        unit_of_measurement: "V"
      ups_nominal_battery_voltage:
        friendly_name: UPS Nominal Battery Voltage
        value_template: "{{ state_attr('sensor.ups', 'NOMBATTV') | regex_replace('[^0-9.]','') | float }}"
        unit_of_measurement: "V"
      ups_time_left:
        friendly_name: UPS Time Left
        value_template: "{{ state_attr('sensor.ups', 'TIMELEFT') | regex_replace('[^0-9.]','') | float }}"
        unit_of_measurement: "min"
```
