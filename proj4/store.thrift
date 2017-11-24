
exception SystemException {
  1: optional string message
}


struct Value {
  1: i32 value;
  2: string content;
  3: double timestamp; // remember, the coordinator sets this
}


service KeyValueStore {
 

  // Client APIs
  Value read(1: i32 key, 2: i32 level),
  void write(1: Value value, 2: i32 level),

  // Internal Replica node APIs
  // replica_name is the name of the node sending the request
  Value get_key(1: i32 key, 2: string from_replica)
    throws (1: SystemException systemException),

  void put_key(1: Value value, 2: string from_replica)
    throws (1: SystemException systemException),


  // tells a replica that it is alive again
  // I might get rid of this
  void ping(1: string replica_name),
}



