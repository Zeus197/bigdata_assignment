trips_df = spark.read.format('csv').options(header='true', inferschema='true').load("/user/hc2660/hw2data/Trips.csv")
fares_df = spark.read.format('csv').options(header='true', inferschema='true').load("/user/hc2660/hw2data/Fares.csv")
#creating table
temp_table_name = "Trips_csv"                                               
trips_df.createOrReplaceTempView(temp_table_name)
temp_table_name2 = "Fares_csv"
fares_df.createOrReplaceTempView(temp_table_name2)
sql_join = "select Trips_csv.medallion, Trips_csv.hack_license, Trips_csv.vendor_id, \
Trips_csv.pickup_datetime, Trips_csv.rate_code, Trips_csv.store_and_fwd_flag, Trips_csv.dropoff_datetime, \
Trips_csv.passenger_count, Trips_csv.trip_time_in_secs, Trips_csv.trip_distance, Trips_csv.pickup_latitude, Trips_csv.pickup_longitude, \
Trips_csv.dropoff_latitude, Trips_csv.dropoff_longitude, Fares_csv.payment_type, Fares_csv.fare_amount, Fares_csv.surcharge, Fares_csv.mta_tax, Fares_csv.tip_amount, \
Fares_csv.tolls_amount, Fares_csv.total_amount from Trips_csv  inner join Fares_csv on Trips_csv.medallion = Fares_csv.medallion AND Trips_csv.hack_license = Fares_csv.hack_license\
 AND Trips_csv.vendor_id = Fares_csv.vendor_id AND Trips_csv.pickup_datetime = Fares_csv.pickup_datetime order by Trips_csv.medallion, Trips_csv.hack_license, Trips_csv.pickup_datetime "
allfare77 = spark.sql(sql_join)
temp_table_name3 = "Alltrips"
allfare77.createOrReplaceTempView(temp_table_name3)

tt22 = "Alltrips"
allfare77.createOrReplaceTempView(tt22)
sql11 = "select Alltrips.fare_amount from Alltrips"
q11 = spark.sql(sql11)

tt23 = "neg_fare"
q11.createOrReplaceTempView(tt23)
sql12 = "select count(*) from neg_fare where fare_amount <0"
q11 = spark.sql(sql12)

xz2 = q11.rdd.map(tuple)
xz3 = xz2.map(lambda r: ','.join([str(KVPair) for KVPair in r])) 
xz4= xz3.map(lambda r: r.replace("'", ""))
xz5 = xz4.map(lambda r: r.replace('(', '').replace(')', '')) 
xz6= xz5.map(lambda r: r.replace("-", ","))
xz6.saveAsTextFile('task3a-sql.out')