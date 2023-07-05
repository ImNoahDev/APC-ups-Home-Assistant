# APC-ups-Home-Assistant
This allows you to broadcast your app UPS information and status from the computer it is connected to, to home assistant

## Usage

### Unraid
If you are on unraid:
Download the USER SCRIPT, PYTHON3 and UNRAID-TMUX plugins then ownload the unraid release of this project

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
