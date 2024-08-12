from db.models.equipment import Equipment

def test_create_equipment():
  eqData = Equipment(id = "station #2")
  
  assert eqData.id == "station #2"