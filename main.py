from flask import Flask, request, render_template, send_file, redirect, url_for, jsonify, abort
from flask_cors import CORS
from threading import Thread
import numpy as np
import atexit
import time
import os

from cleanup import cleanUp
from speed import Speed
from database import videoDB, downDB
import youtube
from model import LR

if __name__ == "__main__":
    atexit.register(cleanUp)
    cleanUp()

    app = Flask(__name__)
    speed = Speed()
    CORS(app)

    speed.getBestServer()
    speed.testDown()

    """예시
    1Gbps 인터넷
    4시간 다시보기: 720p
    10분 영상: 1080p
    
    100Mbps 인터넷
    30분 다큐: 1080p
    3분 MV: 2160p
    """
    X = np.array([[1/1000, 14400], [1/100, 180], [1/1000, 600], [1/100, 1800], [1/100, 36000]]).astype(np.float64)
    Y = np.array([[720], [2160], [1080], [1080], [480]]).astype(np.float64)
    model = LR()
    model.fit(X, Y)

    videos = videoDB()
    downloads = downDB()

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            v = request.form['v']
            v = youtube.get_vid(v)
            return redirect(url_for('download', v=v))
        return render_template('index.html', speed=int(speed.speed))

    @app.route('/download')
    def download():
        v = request.args.get('v', 'dQw4w9WgXcQ')
        v_new = youtube.get_vid(v)
        if v_new != v:
            return redirect(f'/download?v={v_new}')

        return render_template('download.html', v=v, speed=int(speed.speed))

    @app.route('/getinfo/<v>')
    def getinfo(v):
        v_new = youtube.get_vid(v)
        if v_new != v:
            return redirect(f'/getinfo/{v_new}')

        if videos.isOn(v):
            info = videos.get(v)
        else:
            info = youtube.get_info(v)
            videos.push(v, info)
        try:
            info['auto'] = model.predict(np.array([[1/speed.speed, info['dur']]]).astype(np.float64))[0, 0]
        except Exception as e:
            info['auto'] = 720
            print(e)

        return jsonify(info)

    @app.route('/vote/<dur>/<res>')
    def vote(dur, res):
        X = np.array([[1/speed.speed, dur]]).astype(np.float64)
        Y = np.array([[res]]).astype(np.float64)
        model.fit(X, Y)

        v = request.args.get('v', 'dQw4w9WgXcQ')
        return redirect(f'/orange/{v}/{res}')

    @app.route('/orange/<v>/<res>')
    def orange(v, res):
        try:
            v_new = youtube.get_vid(v)
            if v_new != v:
                return redirect(f'/orange/{v_new}/{res}')

            res = int(res)
            res_new = videos.closest(v, res)
            if res_new != res:
                return redirect(f'/orange/{v}/{res_new}')

            status = downloads.get(v, res)
            if status == -1:
                th = Thread(target=youtube.getFile, args=(v, res, downloads))
                th.start()

            time.sleep(1)
            return render_template('orange.html', v=v, res=res, status=status, speed=int(speed.speed))
        except Exception as e:
            print(e)
            return abort(404)


    @app.route('/orange-stat/<v>/<res>')
    def orange_stat(v, res):
        try:
            v_new = youtube.get_vid(v)
            if v_new != v:
                return redirect(f'/orange/{v_new}/{res}')

            res = int(res)
            res_new = videos.closest(v, res)
            if res_new != res:
                return redirect(f'/orange/{v}/{res_new}')

            status = downloads.get(v, res)
            return jsonify({'status': status})
        except Exception as e:
            print(e)
            return abort(404)

    @app.route('/getvideo/<v>/<res>')
    def getvideo(v, res):
        path = os.path.join("download", f'{v}-{res}.mp4')
        try:
            return send_file(path, as_attachment=True)
        except Exception as e:
            print(e)
            return abort(404)

    app.run(host='0.0.0.0')