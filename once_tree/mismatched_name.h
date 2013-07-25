/**
comments
*/

// comments

// file was moved and guard doesn't match file name
#ifndef OLD_THING_H
#define OLD_THING_H

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









#endif

