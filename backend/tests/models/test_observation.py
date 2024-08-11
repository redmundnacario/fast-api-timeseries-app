from db.models.observation import Observation
from db.models.equipment import Equipment

def test_create_observation():
  obsData = Observation(equipmentId = 2, 
                        timestamp = "2024-08-11T08:30:17.307Z", 
                        value = 2,
                        flag = "valid")
  
  assert obsData.equipmentId == 2
  assert obsData.timestamp == "2024-08-11T08:30:17.307Z"
  assert obsData.value == 2
  assert obsData.flag == "valid"
  
# def test_equipment_obsevation_relationship():
#   eqData = Equipment(name = "station #2")
#   obsData = Observation(timestamp = "2024-08-11T08:30:17.307Z", 
#                         value = 2,
#                         flag = "valid", equipment = eqData)
#   assert obsData.equipmentName == eqData