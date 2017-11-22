
exception SystemException {
  1: optional string message
}


struct Value {
  1: i32 value;
  2: string content;
  3: double timestamp; // remember, the coordinator sets this
}


service KeyValueStore {
  
  // RPC used by clients
  Value get_key(1: i32 level)
    throws (1: SystemException systemException),

  
  // RPC used by clients
  void put_key_value(1: Value value, 2: i32 level)
    throws (1: SystemException systemException),



  // RPC used between replicas.
  // tells a replica that it is alive again
  void ping(1: string replica_name),


}



