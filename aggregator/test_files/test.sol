pragma solidity ^0.4.18;

contract sensor_enrollment {
    struct sensor_info {
        string merkle_root;
    }

    struct enrollment_info {
        string key;
    }

    mapping(string => mapping(string => sensor_info)) tag_to_token;
    mapping(string => enrollment_info) token_to_key;

    function StoreSensorData(
        string token_,
        string tag_,
        string data_
    ) public {
        sensor_info storage location = tag_to_token[tag_][token_];
        location.merkle_root = data_;
    }

    function RetrieveSensorData(string token_, string tag_)
        public
        view
        returns (string)
    {
        sensor_info storage location = tag_to_token[tag_][token_];
        return (location.merkle_root);
    }

    function StoreEnrollmentData(string id_, string key_) public {
        enrollment_info storage location = token_to_key[id_];
        location.key = key_;
    }

    function RetrieveEnrollmentData(string id_) public view returns (string) {
        enrollment_info storage location = token_to_key[id_];
        return (location.key);
    }
}
