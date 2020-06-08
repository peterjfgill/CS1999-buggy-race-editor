from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
app = Flask(__name__)

DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"

BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"


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
  if request.method == 'GET':
    return render_template("buggy-form.html")
  elif request.method == 'POST':
    msg=""
    try:
      qty_wheels = request.form['qty_wheels']
      flag_color = request.form['flag_color']
      flag_color_secondary = request.form['flag_color_secondary']
      flag_pattern = request.form['flag_pattern']
      power_type = request.form['power_type']
      power_units = request.form['power_units']
      aux_power_type = request.form['aux_power_type']
      aux_power_units = request.form['aux_power_units']
      hamster_booster = request.form['hamster_booster']
      tyres = request.form['tyres']
      qty_tyres = request.form['qty_tyres']
      armour = request.form['armour']
      attack = request.form['attack']
      qty_attack = request.form['qty_attack']
      fireproof = request.form['fireproof']
      insulated = request.form['insulated']
      antibiotic = request.form['antibiotic']
      banging = request.form['banging']
      algo = request.form['algo']

      msg = f"qty_wheels={qty_wheels}, flag_color={flag_color} , flag_color_secondary={flag_color_secondary}, flag_pattern={flag_pattern}, power_type={power_type}, power_units={power_units}, aux_power_type={aux_power_type}, aux_power_units={aux_power_units}, hamster_booster={hamster_booster}, tyres={tyres}, qty_tyres={qty_tyres}, armour={armour}, attack={attack}, qty_attack={qty_attack}, fireproof={fireproof}, insulated={insulated}, antibiotic={antibiotic}, banging={banging}, algo={algo}"

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
        cur.execute("UPDATE buggies set qty_attack=? WHERE id=?", (qty_attack, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set fireproof=? WHERE id=?", (fireproof, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set insulated=? WHERE id=?", (insulated, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set antibiotic=? WHERE id=?", (antibiotic, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set banging=? WHERE id=?", (banging, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set algo=? WHERE id=?", (algo, DEFAULT_BUGGY_ID))
        con.commit()
        msg = "Record successfully saved"
    except:
      con.rollback()
      msg = "error in update operation"
    finally:
      con.close()
      return render_template("updated.html", msg = msg)

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
