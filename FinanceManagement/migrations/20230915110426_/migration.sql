/*
  Warnings:

  - You are about to drop the column `from` on the `UserTransaction` table. All the data in the column will be lost.
  - You are about to drop the column `to` on the `UserTransaction` table. All the data in the column will be lost.
  - Added the required column `from_user` to the `UserTransaction` table without a default value. This is not possible if the table is not empty.
  - Added the required column `to_user` to the `UserTransaction` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "UserTransaction" DROP COLUMN "from",
DROP COLUMN "to",
ADD COLUMN     "from_user" TEXT NOT NULL,
ADD COLUMN     "to_user" TEXT NOT NULL;
