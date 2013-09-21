/**
comments
*/

// comments

#ifndef PARTIALLYMATCHEDGUARD_H_THIS_PART_DOESNT_MATCH
#define PARTIALLYMATCHEDGUARD_H_THIS_PART_DOESNT_MATCH

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
