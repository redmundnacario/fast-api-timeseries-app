from db.models.equipment import Equipment

def test_create_equipment():
  eqData = Equipment(name = "station #2")
  
  assert eqData.name == "station #2"