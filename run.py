from hearatale import app

if app.config['PROD']:
    app.run(host="0.0.0.0")
else:
    app.run(host='0.0.0.0', debug=True)