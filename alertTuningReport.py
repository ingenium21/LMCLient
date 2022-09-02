import json
import sys
from pprint import pprint
sys.path.append("./")
from LMClient.LMClient import LMClient
import pandas
import os
from dotenv import load_dotenv

load_dotenv()



def get_devices(client):
    """
    Get all devices
    """
    devices = client.get('/device/devices', queryParam='?size=500')
    devices = devices['items']
    return devices

def crawl_devices(client, devices):
    """
    Crawl all devices
    """
    for device in devices:
        device_id = device['id']
        get_device_info(client, device_id)

def get_device_info(client, device_id):
    """
    uses the device id to get device info
    """
    device_info = client.get('/device/{}'.format(device_id))
    return device_info

def get_device_groups(client, device_id):
    """
    uses the device id to get all groups pertaining to that device
    """
    groups = client.get('/device/{}/groups'.format(device_id))
    groups = groups['items']
    return groups



def get_device_datasources(client, device_id):
    """
    uses the device id to get all datasources pertaining to that device
    """
    datasources = client.get('/device/{}/datasources'.format(device_id))
    datasources = datasources['items']
    return datasources

def get_device_property(device):
    """
    Get the device property
    """
    propArray = []
    for prop in device['systemProperties']:
            if prop['name'] == 'system.sysinfo':
                #if propvalue regex matches pattern, assign match to propvalue
                propvalue = prop['value']
                if propvalue.find('Silver Peak Systems, Inc') != -1:
                    slicedValue = "Silver Peak Device"
                    prop['value'] = slicedValue
                if propvalue.find('Cisco') != -1:
                    slicedValue = "Cisco Device"
                    prop['value'] = slicedValue
                if propvalue.find('Windows') != -1:
                    slicedValue = "Windows Device"
                    prop['value'] = slicedValue
                if propvalue.find('Linux') != -1:
                    slicedValue = "Linux Device"
                    prop['value'] = slicedValue
                if propvalue.find('Palo Alto Networks') != -1:
                    slicedValue = "Palo Alto Networks Device"
                    prop['value'] = slicedValue
                if propvalue.find('Meraki') != -1:
                    slicedValue = "Meraki Device"
                    prop['value'] = slicedValue
                if propvalue.find('VMware') != -1:
                    slicedValue = "VMware Device"
                    prop['value'] = slicedValue

                if prop['value'] not in propArray:
                    propArray.append(prop['value'])
    return propArray

def separate_device_by_type(groupName):
    """ Separates the string Devices by Type/etc"""
    #return everything after the last '/'
    return groupName.split('Devices by type/')[1]

def get_device_groups(systemProperties):
    """
    Get the device groups
    """
    groups = []
    for prop in systemProperties:
        if prop['name'] == 'system.groups':
            groups = (prop['value']).split(',')
    return groups

def remove_unecessary_device_groups(groups):
    """
    Removes the unnecessary device groups
    """
    for group in groups:
        if group.find('Devices by Type') == -1 or group.lower().find('Ironbow'.lower()) != -1:
            groups.remove(group)
    return groups

def get_datasources(client, device_id):
    """
    Get the datasources
    """
    datasources = client.get('/device/devices/{}/devicedatasources'.format(device_id), queryParam='?size=500')
    datasources = datasources['items']
    return datasources



def add_datasources_to_deviceType(deviceTypes, datasources, device_groups):
    for deviceType in deviceTypes:
        deviceTypeDict = deviceTypes[deviceType]
        for device_group in device_groups:
            #if deviceType string is found in device_group, add to datasources
            if deviceType.lower() in device_group.lower():
                for ds in datasources:
                    hdsid = ds['dataSourceId']
                    if hdsid not in deviceTypeDict['datasources']:
                        dsdict = {hdsid: ds}
                        deviceTypeDict['datasources'].append(dsdict)

def get_device_alertsettings(client, device_id):
    """
    Get the device alertsettings
    """
    alertsettings = client.get('/device/devices/{}/alertsettings'.format(device_id))
    return alertsettings

if __name__ == '__main__':
    account = os.getenv("ACCOUNT")
    accessID = os.getenv('ACCESSID')
    accessKey = os.getenv('ACCESSKEY')
    client = LMClient(account, accessID, accessKey)
    deviceTypes = {"Windows":{'datasources' : []}, "Linux":{'datasources' : []}, "Cisco":{'datasources' : []}, "Palo Alto Networks":{'datasources' : []}, "Meraki":{'datasources' : []}, "VMware":{'datasources' : []}, "Silver Peak":{'datasources' : []}}
    datasources = []
    devices = get_devices(client)
    pprint(devices)
    for device in devices:
        isCollector = False
        device_id = device['id']
        systemProperties = device['systemProperties']
        for prop in systemProperties:
            if prop['name'] == 'system.collector':
                if prop['value'] == 'true' or prop['value'] == True:
                    isCollector = True
        if isCollector:
            continue
        # alertSettings = get_device_alertsettings(client, device_id)
        # pprint(alertSettings)
        
        
    pprint(deviceTypes)