from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
app = Flask(__name__)

DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"

BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"

power_type_costs = {
  "none"        : 0,
  "petrol"      : 4,
  "fusion"      : 400,
  "steam"       : 3,
  "bio"         : 5,
  "electric"    : 20,
  "rocket"      : 16,
  "hamster"     : 3,
  "nuclear"     : 300,
  "solar"       : 40,
  "wind"        : 20
}
tyre_costs = {
  "knobbly"     : 15,
  "slick"       : 10,
  "steelband"   : 20,
  "reactive"    : 40,
  "maglev"      : 50
}
armour_costs = {
  "none"        : 0,
  "wood"        : 40,
  "aluminium"   : 200,
  "thinsteel"   : 100,
  "thicksteel"  : 200,
  "titanium"    : 290
}
attack_costs = {
  "none"        : 0,
  "spike"       : 5,
  "flame"       : 20,
  "charge"      : 28,
  "biohazard"   : 30
}


#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@app.route('/')
def home():
   return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@app.route('/new', methods = ['POST', 'GET'])
def create_buggy():

  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies")
  record = cur.fetchone();

  if request.method == 'GET':
    return render_template("buggy-form.html", buggy = record)
    
  elif request.method == 'POST':
    msg=""
    error = False
    total_cost = 0
   

    qty_wheels = request.form['qty_wheels']
    if qty_wheels.isdigit():
      if (int(qty_wheels) % 2 != 0):
        msg += f"{qty_wheels} is not a valid input for the number of wheels, please input an even number.\n"
        error = True
    else:
      msg += f"{qty_wheels} is not a valid input for the number of wheels.\n"
      error = True
    
    flag_color = (request.form['flag_color']).strip("")
    flag_color_secondary = (request.form['flag_color_secondary']).strip("")
    flag_pattern = (request.form['flag_pattern']).strip("")

    if flag_color_secondary == flag_color and flag_pattern != "plain":
      msg += f"The primary and secondary colors of the flag must be different unless the pattern is plain."
      error = True

    power_type = (request.form['power_type']).strip("")

    power_units = request.form['power_units']
    if power_units.isdigit():
      if int(power_units) < 0:
        msg += f"Please input a number greater than or equal to 0.\n "
        error = True
    else:
      msg += f"{power_units} is not a valid input for the primary motive power units.\n "
      error = True

    aux_power_type = (request.form['aux_power_type']).strip("")

    if aux_power_type == "none":
      aux_power_units = 0
    else:
      aux_power_units = request.form['aux_power_units']
      if aux_power_units.isdigit():
        if int(aux_power_units) < 0:
          msg += f"Please input a number greater than or equal to 0.\n "
          error = True
      else:
        msg += f"{aux_power_units} is not a valid input for the primary motive power units.\n "
        error = True

    hamster_booster = request.form['hamster_booster']
    if power_type == "hamster" or aux_power_type == "hamster":
      if not hamster_booster.isdigit():
        msg += f"{hamster_booster} is not a valid input for hamster booster.\n "
        error = True
    else:
      hamster_booster = 0
    
    tyres = (request.form['tyres']).strip("")

    qty_tyres = request.form['qty_tyres']
    if qty_tyres.isdigit():
      if int(qty_tyres) < int(qty_wheels):
        msg += f"Quantity of tyres must be equal to or greater than the quantity of wheels.\n "
        error = True
    else:
      msg += f"{qty_tyres} is not a valid input for the number of tyres.\n "
      error = True

    armour = (request.form['armour']).strip("")

    attack = (request.form['attack']).strip("")

    qty_attacks = request.form['qty_attacks']
    if not qty_wheels.isdigit():
      msg += f"{qty_attacks} is not a valid input for the number of attacks.\n"
      error = True

    fireproof = ((request.form['fireproof']).strip("")).lower()
    if fireproof != "false" and fireproof != "true":
      msg += f"{fireproof} is not a valid input for whether or not the buggy is fireproof.\n"
      error = True
    if fireproof == "true":
      total_cost += 70

    insulated = ((request.form['insulated']).strip("")).lower()
    if insulated != "false" and insulated != "true":
      msg += f"{insulated} is not a valid input for whether or not the buggy is insulated.\n"
      error = True
    if insulated == "true":
      total_cost += 100

    antibiotic = ((request.form['antibiotic']).strip("")).lower()
    if antibiotic != "false" and antibiotic != "true":
      msg += f"{antibiotic} is not a valid input for whether or not the buggy is antibiotic.\n"
      error = True
    if antibiotic == "true":
      total_cost += 90

    banging = ((request.form['banging']).strip("")).lower()
    if banging != "false" and banging != "true":
      msg += f"{banging} is not a valid input for whether or not the buggy is banging.\n"
      error = True
    if banging == "true":
      total_cost += 42
  
    algo = (request.form['algo']).strip("")

    buggy_cost_limit = request.form.get('buggy_cost_limit', 400)

    total_cost += (power_type_costs[power_type] * int(power_units))
    total_cost += (power_type_costs[aux_power_type] * int(aux_power_units))
    total_cost += (tyre_costs[tyres] * int(qty_tyres))
    total_cost += (armour_costs[armour]) + (armour_costs[armour] * (int(qty_wheels)-4) * 0.1)
    total_cost += (attack_costs[attack] * int(qty_attacks))
    total_cost += (int(hamster_booster)*5)



    if total_cost > buggy_cost_limit:
      msg += f"Please adjust your buggy until the total cost is less than {buggy_cost_limit}.\n"
      error == True

    if error == True:
      return render_template("buggy-form.html", msg = msg, buggy = record)

    try:          
      
      

      msg = f"qty_wheels={qty_wheels}, flag_color={flag_color} , flag_color_secondary={flag_color_secondary}, flag_pattern={flag_pattern}, power_type={power_type}, power_units={power_units}, aux_power_type={aux_power_type}, aux_power_units={aux_power_units}, hamster_booster={hamster_booster}, tyres={tyres}, qty_tyres={qty_tyres}, armour={armour}, attack={attack}, qty_attacks={qty_attacks}, fireproof={fireproof}, insulated={insulated}, antibiotic={antibiotic}, banging={banging}, algo={algo}, total_cost={total_cost}, buggy_cost_limit={buggy_cost_limit}"

      with sql.connect(DATABASE_FILE) as con:
        cur = con.cursor()
        cur.execute("UPDATE buggies set qty_wheels=? WHERE id=?", (qty_wheels, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set flag_color=? WHERE id=?", (flag_color, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set flag_color_secondary=? WHERE id=?", (flag_color_secondary, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set flag_pattern=? WHERE id=?", (flag_pattern, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set power_type=? WHERE id=?", (power_type, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set power_units=? WHERE id=?", (power_units, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set aux_power_type=? WHERE id=?", (aux_power_type, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set aux_power_units=? WHERE id=?", (aux_power_units, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set hamster_booster=? WHERE id=?", (hamster_booster, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set tyres=? WHERE id=?", (tyres, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set qty_tyres=? WHERE id=?", (qty_tyres, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set armour=? WHERE id=?", (armour, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set attack=? WHERE id=?", (attack, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set qty_attacks=? WHERE id=?", (qty_attacks, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set fireproof=? WHERE id=?", (fireproof, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set insulated=? WHERE id=?", (insulated, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set antibiotic=? WHERE id=?", (antibiotic, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set banging=? WHERE id=?", (banging, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set algo=? WHERE id=?", (algo, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set total_cost=? WHERE id=?", (total_cost, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set buggy_cost_limit=? WHERE id=?", (buggy_cost_limit, DEFAULT_BUGGY_ID))
        con.commit()
        msg = "Record successfully saved"
    except:
      con.rollback()
      msg = "error in update operation"
    finally:
      con = sql.connect(DATABASE_FILE)
      con.row_factory = sql.Row
      cur = con.cursor()
      cur.execute("SELECT * FROM buggies")
      record = cur.fetchone(); 
      con.close()
      return render_template("updated.html", msg = msg, buggy = record)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies")
  record = cur.fetchone(); 
  return render_template("buggy.html", buggy = record)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/new')
def edit_buggy():
  return render_template("buggy-form.html")


#------------------------------------------------------------
# get JSON from current record
#   this is still probably right, but we won't be
#   using it because we'll be dipping diectly into the
#   database
#------------------------------------------------------------
@app.route('/json')
def summary():
  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))
  return jsonify(
      {k: v for k, v in dict(zip(
        [column[0] for column in cur.description], cur.fetchone())).items()
        if (v != "" and v is not None)
      }
    )

#------------------------------------------------------------
# delete the buggy
#   don't want DELETE here, because we're anticipating
#   there always being a record to update (because the
#   student needs to change that!)
#------------------------------------------------------------
@app.route('/delete', methods = ['POST'])
def delete_buggy():
  try:
    msg = "deleting buggy"
    with sql.connect(DATABASE_FILE) as con:
      cur = con.cursor()
      cur.execute("DELETE FROM buggies")
      con.commit()
      msg = "Buggy deleted"
  except:
    con.rollback()
    msg = "error in delete operation"
  finally:
    con.close()
    return render_template("updated.html", msg = msg)


if __name__ == '__main__':
   app.run(debug = True, host="0.0.0.0")
