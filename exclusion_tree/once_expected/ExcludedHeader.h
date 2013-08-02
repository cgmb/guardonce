/**
comments
*/

// comments

#pragma once

// Comments!
#include <vector>
#include "MyOtherThing.h"

class Thing
{
public:
   explict Thing();
   virtual ~Thing();

   bool operator==(const Thing& rhs);
   bool operator!=(const Thing& rhs);

private:
   std::vector<int> stuff_;
};










