#!/bin/bash

# Creates a filtered version of gtfs files.  gtfs dumps for NSW are very large
# (around 1GB expanded).  This script allows for filtering of the gtfs data
# for just the records for particular agencies.

# This requires a running postgresql server running on the local machine.

# Agency id's that are to be kept.
# To find the id's to be kept look in the agency.txt file in the gtfs downloads.
AGENCY_LIST="('34', 'add-more-here')"

function usage() {
   echo "$0: gtfs_zip_file result_gtfs_file.zip" 1>&2
   exit 1
}

if [ x$1 == x ]; then
  echo "Missing first arg (input file):" 1>&2
  usage
fi

INPUT_FILE="$1"

if [ ! -f "$INPUT_FILE" ]; then
  echo "Missing input file: $INPUT_FILE" 1>&2
  usage
fi

if [ x$2 == x ]; then
  echo "Missing second arg (outout file):" 1>&2
  usage
fi

OUTPUT_FILE="$2"

function run_filter() {

local inf="$1"
local outf="$2"

psql <<MARKER
begin;

-- agency.txt
drop table if exists agency cascade;
create table agency (agency_id text NOT NULL PRIMARY KEY,agency_name text,agency_url text,agency_timezone text,agency_lang text,agency_phone text);
copy agency from '$inf/agency.txt' DELIMITER ',' CSV HEADER;

-- calendar_dates.txt
drop table if exists calendar_dates cascade;
create table calendar_dates (service_id text,date text,exception_type text);
copy calendar_dates from '$inf/calendar_dates.txt' DELIMITER ',' CSV HEADER;
create unique index calendar_dates_i1 on calendar_dates (service_id, date, exception_type);

-- calendar.txt
drop table if exists calendar cascade;
create table calendar (service_id text,monday text,tuesday text,wednesday text,thursday text,friday text,saturday text,sunday text,start_date text,end_date text);
copy calendar from '$inf/calendar.txt' DELIMITER ',' CSV HEADER;
create unique index calendar_i1 on calendar (service_id, start_date);

-- routes.txt
drop table if exists routes cascade;
create table routes (route_id text NOT NULL PRIMARY KEY,agency_id text REFERENCES agency ON DELETE CASCADE,route_short_name text,route_long_name text,route_desc text,route_type text,route_color text,route_text_color text);
copy routes from '$inf/routes.txt' DELIMITER ',' CSV HEADER;

-- shapes.txt
drop table if exists shapes cascade;
create table shapes (shape_id text,shape_pt_lat text,shape_pt_lon text,shape_pt_sequence text,shape_dist_traveled text);
copy shapes from '$inf/shapes.txt' DELIMITER ',' CSV HEADER;
create unique index shapes_i1 on shapes (shape_id, shape_pt_sequence);

-- stops.txt
drop table if exists stops cascade;
create table stops (stop_id text NOT NULL PRIMARY KEY,stop_code text,stop_name text,stop_lat text,stop_lon text,location_type text,parent_station text,wheelchair_boarding text,platform_code text);
copy stops from '$inf/stops.txt' DELIMITER ',' CSV HEADER;

-- trips.txt
drop table if exists trips cascade;
create table trips (route_id text REFERENCES routes ON DELETE CASCADE,service_id text,trip_id text NOT NULL PRIMARY KEY,shape_id text,trip_headsign text,direction_id text,block_id text,wheelchair_accessible text);
copy trips from '$inf/trips.txt' DELIMITER ',' CSV HEADER;
create index trips_i1 on trips (shape_id, route_id);

-- stop_times.txt
drop table if exists stop_times cascade;
create table stop_times (trip_id text REFERENCES trips ON DELETE CASCADE,arrival_time text,departure_time text,stop_id text,stop_sequence text,stop_headsign text,pickup_type text,drop_off_type text,shape_dist_traveled text);
copy stop_times from '$inf/stop_times.txt' DELIMITER ',' CSV HEADER;
create unique index stop_times_i1 on stop_times (trip_id, stop_sequence);
create index stop_times_i2 on stop_times (stop_id);

commit;

begin;
-- Delete agencies, routes, trips and stop_times
delete from agency where agency_id not in $AGENCY_LIST;
commit;

begin;
-- Delete stop ids that are not used.
delete from stops where stop_id not in (select st.stop_id from stop_times st where st.stop_id = stop_id);
commit;

begin;
-- Delete shape ids that are not used.
delete from shapes where shape_id not in (select trips.shape_id from trips where trips.shape_id = shape_id);
commit;

COPY agency TO '$outf/agency.txt' DELIMITER ',' CSV HEADER;
COPY calendar TO '$outf/calendar.txt' DELIMITER ',' CSV HEADER;
COPY calendar_dates TO '$outf/calendar_dates.txt' DELIMITER ',' CSV HEADER;
COPY routes TO '$outf/routes.txt' DELIMITER ',' CSV HEADER;
COPY shapes TO '$outf/shapes.txt' DELIMITER ',' CSV HEADER;
COPY stop_times TO '$outf/stop_times.txt' DELIMITER ',' CSV HEADER;
COPY stops TO '$outf/stops.txt' DELIMITER ',' CSV HEADER;
COPY trips TO '$outf/trips.txt' DELIMITER ',' CSV HEADER;

-- Creates a special table so we can avoid loading stop_times which is huge.
COPY (select distinct route_id, stop_id from trips, stop_times where trips.trip_id = stop_times.trip_id) to '$outf/trips_stops.txt' DELIMITER ',' CSV HEADER;

-- Create a pre-processed table containing headsigns and the return headsign.
COPY (select distinct route_short_name, t1.route_id, t1.direction_id, t1.trip_headsign, t2.trip_headsign as trip_headsign_return from routes, trips as t1, trips as t2 where t1.route_id = t2.route_id and t1.direction_id <> t2.direction_id and t1.trip_headsign <> t2.trip_headsign and routes.route_id = t1.route_id order by t1.route_id) to '$outf/trips_headsigns.txt' DELIMITER ',' CSV HEADER;


MARKER
}

function abspath () {
  case "$1" in
    /*) printf "%s\n" "$1";;
    *) printf "%s\n" "$PWD/$1";;
  esac;
}

declare -a on_exit_items

function on_exit()
{
    for i in "${on_exit_items[@]}"
    do
        echo "on_exit: $i"
        eval $i
    done
}

function add_on_exit()
{
    local n=${#on_exit_items[*]}
    on_exit_items[$n]="$*"
    if [[ $n -eq 0 ]]; then
        echo "Setting trap"
        trap on_exit EXIT
    fi
}

TMP_IN_DIR=`mktemp -d`
add_on_exit rm -rf $TMP_IN_DIR
chmod a+rx $TMP_IN_DIR

TMP_OUT_DIR=`mktemp -d`
add_on_exit rm -rf $TMP_OUT_DIR
chmod a+rwx $TMP_OUT_DIR


if ! unzip -x -d $TMP_IN_DIR $INPUT_FILE; then
  echo "Input file unzip failed '$INPUT_FILE':" 1>&2
  exit 1
fi

if ! run_filter $TMP_IN_DIR $TMP_OUT_DIR; then
  echo "Filter failed." 1>&2
  exit 1
fi

ABS_OUT="`abspath $OUTPUT_FILE`"

if ! (cd $TMP_OUT_DIR && zip "$ABS_OUT" *.txt); then
  echo "Input file unzip failed '$INPUT_FILE':" 1>&2
  exit 1
fi

# Success.

