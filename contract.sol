pragma solidity ^0.4.18;

contract Person {

   string fName;
   uint age;

   function setInfo(string _fName, uint _age) public {
       fName = _fName;
       age = _age;
   }

   function getInfo() public constant returns (string, uint) {
       return (fName, age);
   }
    
}
