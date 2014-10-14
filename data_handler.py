from obspy.imaging.beachball import Beachball
from flask import g

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

def parse_data():
	raw_data = open('static/all_events.txt').readlines()
	earthquakes = list(chunker(raw_data, 5))

	event_names = [eq[1][:16].strip() for eq in earthquakes]

	lat_arrays = [eq[0].strip().split() for eq in earthquakes]
	latitudes = [float(arr[3]) for arr in lat_arrays]

	long_arrays = [eq[0].strip().split() for eq in earthquakes]
	longitudes = [float(arr[4]) for arr in long_arrays]

	mt_arrays = [eq[3].strip().split() for eq in earthquakes]
	moment_tensors = [[float(el) for el in arr[1::2]] for arr in mt_arrays]

	sdr_arrays = [eq[4].strip().split() for eq in earthquakes]
	strike_dip_rakes = [[float(el) for el in arr[11:14]] for arr in sdr_arrays]

	data = zip(event_names, latitudes, longitudes, moment_tensors, strike_dip_rakes)
	return data

def draw_beachballs():
	data = parse_data()
	for event in list(data):
		try:
			Beachball(event[3], facecolor='r', outfile='static/' + event[0] + '.png')
		except IndexError:
			Beachball(event[4], facecolor='r', outfile='static/' + event[0] + '.png')
			print "One of the moment tensor components was 0. Using strike/dip/rake values for event" + event[0]

def add_db_records(db):
	data = parse_data()
	for event in list(data):
		db.execute('insert into earthquakes (event_name, latitude, longitude, moment_tensor, strike_dip_rake) values (?, ?, ?, ?, ?)', [event[0], event[1], event[2], str(event[3]), str(event[4])])
		db.commit()