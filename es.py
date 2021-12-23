
from dataclasses import dataclass
import csv


@dataclass(frozen=True, eq=True)
class StorageMedium:
    name: str
    energy_density: float

@dataclass(frozen=True, eq=True)
class Transformation:
    name: str
    power_flux: float

@dataclass
class Device:
    name: str
    storage_medium: StorageMedium
    transformation: Transformation

def read_devices():
    storage_media = {}
    with open('storagemedia.csv') as f:
        reader = csv.reader(f)
        headers = next(reader) 
        for row in reader:
            storage_media[row[0]] = StorageMedium(
                row[0], 
                float(row[1])
                )

    transformations = {}
    with open('transdevices.csv') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            transformations[row[0]] = Transformation(
                row[0], 
                float(row[1])
                )


    devices = {}
    with open('technologies.csv') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            devices[row[0]] = Device(
                row[0],
                storage_media[row[1]],     
                transformations[row[2]]
                )
            
    return devices