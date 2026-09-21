import sqlite3
import os
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'




import sqlite3
import os
from flask import Flask, render_template, request

app = Flask(__name__)