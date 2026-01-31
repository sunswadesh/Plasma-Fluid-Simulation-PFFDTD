#include <gtest/gtest.h>
#include "utils/constants.h"
#include <cmath>

TEST(ConstantsTest, PhysicalConstants) {
    EXPECT_NEAR(PI, 3.14159265359, 1e-10);
    EXPECT_NEAR(C, 2.998e8, 1.0);
    EXPECT_NEAR(MU_0, 1.25663706e-6, 1e-13);
}
