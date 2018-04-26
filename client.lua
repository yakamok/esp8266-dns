sk = net.createConnection(net.UDP, 0)
ens = “zz1.”
ene = “.xx1.”
data = "hello"
server_address = ".ns.example.com"
sensor_data = ens .. data .. ene .. server_address
sk:dns(sensor_data,function(conn,ip) end)
sk = nil
