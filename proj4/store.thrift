
exception SystemException {
  1: optional string message
}


struct Value {
  1: i32 key;
  2: string content;
  3: double timestamp; // remember, the coordinator sets this
}


service KeyValueStore {
 

  // Client APIs
  Value read(1: i32 key, 2: i32 level)
    throws (1: SystemException systemException),
  void write(1: Value value, 2: i32 level)
    throws (1: SystemException systemException),

  // Internal Replica node APIs
  // replica_name is the name of the node sending the request
  Value get_key(1: i32 key, 2: string from_replica),

  void put_key(1: Value value, 2: string from_replica),

}



