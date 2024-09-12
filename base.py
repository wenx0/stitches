import math

class Block:
    ROW_NUM = "ROW {}"
    CAST_ON = "Cast on {} {}"
    KNIT_REG = "Knit {} row(s)"
    KNIT_BOTH = "Knit {} row(s) - {} one stitch each side every {} rows, until {} total stitches"
    KNIT_ONE = "Knit {} row(s) - {} one stitch on the {} every {} rows, until {} total stitches"

    def __init__(self, gaugeStitches, gaugeRows):
        self.gaugeStitches = gaugeStitches
        self.gaugeRows = gaugeRows

    @classmethod
    def makeBlock(cls, Block):
        return cls(Block.gaugeStitches, Block.gaugeRows)

    def convertWidth(self, width):
        return int(round(width * (self.gaugeStitches / 4)))

    def convertLength(self, length):
        return int(round(length * (self.gaugeRows / 4)))

    def add_instruction(self, instructions, instruction):
        instructions.append(instruction)

class Shape(Block):
    def setup(self, length, startwidth, endwidth=-1):
        if endwidth == -1:
            endwidth = startwidth

        self.startWidthSt = self.convertWidth(startwidth)
        self.endWidthSt = self.convertWidth(endwidth)
        self.lengthRows = self.convertLength(length)

        self.totalRC = self.lengthRows
        self.isSquare = self.startWidthSt == self.endWidthSt

        if not self.isSquare:
            self.change = "increasing" if self.startWidthSt < self.endWidthSt else "decreasing"
            delta = float(abs(self.startWidthSt - self.endWidthSt)) / 2.0 + 1
            self.cadence = int(math.floor(float(self.totalRC) / float(delta)))

    def printCastOn(self, instructions, extra=None):
        self._printCastOn(instructions, self.startWidthSt, extra)

    def printHalfCastOn(self, instructions, extra=None):
        self._printCastOn(instructions, int(self.startWidthSt / 2), extra)

    def _printCastOn(self, instructions, width, extra):
        self.add_instruction(instructions, self.ROW_NUM.format(0))
        self.add_instruction(instructions, self.CAST_ON.format(width, extra))

    def printInstructions(self, instructions, startRC=0):
        return self._printInstructions(startRC, self.endWidthSt, instructions)

    def printHalfInstructions(self, instructions, startRC=0, side="Right"):
        return self._printInstructions(startRC, int(self.endWidthSt / 2), instructions, side=side)

    def _printInstructions(self, startRC, endWidthSt, instructions, side=None):
        if self.isSquare:
            self.add_instruction(instructions, self.KNIT_REG.format(self.lengthRows))
        elif not side:
            self.add_instruction(instructions, self.KNIT_BOTH.format(self.lengthRows, self.change, self.cadence, endWidthSt))
        else:
            self.add_instruction(instructions, self.KNIT_ONE.format(self.lengthRows, self.change, side, self.cadence, endWidthSt))

        rc = int(self.totalRC + startRC)
        self.add_instruction(instructions, self.ROW_NUM.format(rc))
        return rc


class Sleeve(Block):
    def setup(self, chestCircumferenceIn, cuffRibbingIn=2, ribbingBlock=None,
              wristCircumferencePct=0.2, lowerLengthPct=0.5, lowerSleeveWidthPct=0.35,
              armpitDecreasePct=0.025, upperWidthPct=0.1, upperHeightPct=0.2):

        self.chestCircumference = chestCircumferenceIn
        self.armpitDecreasePct = armpitDecreasePct
        if not ribbingBlock:
            ribbingBlock = self

        upperSleeveLength = upperHeightPct * chestCircumferenceIn
        remainingLowerSleeveLength = lowerLengthPct * chestCircumferenceIn

        if cuffRibbingIn > 0:
            self.cuffRibbing = Shape.makeBlock(ribbingBlock)
            self.cuffRibbing.setup(cuffRibbingIn, chestCircumferenceIn * wristCircumferencePct)
            remainingLowerSleeveLength = remainingLowerSleeveLength - cuffRibbingIn

        lowerSleeveTopHeight = chestCircumferenceIn * armpitDecreasePct
        self.lowerSleeveTop = Shape.makeBlock(self)
        self.lowerSleeveTop.setup(lowerSleeveTopHeight, chestCircumferenceIn * lowerSleeveWidthPct)
        remainingLowerSleeveLength = remainingLowerSleeveLength - lowerSleeveTopHeight

        self.lowerSleeve = Shape.makeBlock(self)
        self.lowerSleeve.setup(remainingLowerSleeveLength,
                               chestCircumferenceIn * wristCircumferencePct,
                               chestCircumferenceIn * lowerSleeveWidthPct)

        upperSleeveWidthPct = lowerSleeveWidthPct - (2.0 * armpitDecreasePct)
        self.upperSleeve = Shape.makeBlock(self)
        self.upperSleeve.setup(upperSleeveLength,
                               chestCircumferenceIn * upperSleeveWidthPct,
                               chestCircumferenceIn * upperWidthPct)

    def printInstructions(self, instructions):
        self.add_instruction(instructions, "Sleeve worked bottom up, make 2:")
        runningRC = 0
        if self.cuffRibbing:
            self.cuffRibbing.printCastOn(instructions, "for 1x1 ribbing")
            runningRC = self.cuffRibbing.printInstructions(instructions, runningRC)
            self.add_instruction(instructions, "Now for the stockinette section")
        else:
            self.lowerSleeve.printCastOn(instructions)

        runningRC = self.lowerSleeve.printInstructions(instructions, runningRC)
        self.add_instruction(instructions, f"Cast off {self.convertWidth(self.armpitDecreasePct * self.chestCircumference)} on each side")
        runningRC = self.upperSleeve.printInstructions(instructions, runningRC)


class BodyPannel(Block):
    def setup(self, chestCircumferenceIn, bottomRibbingIn=2, ribbingBlock=None,
              bottomLengthPct=0.5, widthPct=0.5, armpitDecreasePct=0.05, upperHeightPct=0.25,
              neckWidthPct=0.15):

        self.chestCircumference = chestCircumferenceIn
        self.armpitDecreasePct = armpitDecreasePct

        if not ribbingBlock:
            ribbingBlock = self

        remainingBottomLength = bottomLengthPct * chestCircumferenceIn

        if bottomRibbingIn > 0:
            self.bottomRibbing = Shape.makeBlock(ribbingBlock)
            self.bottomRibbing.setup(bottomRibbingIn, chestCircumferenceIn * widthPct)
            remainingBottomLength = remainingBottomLength - bottomRibbingIn

        self.bottom = Shape.makeBlock(self)
        self.bottom.setup(remainingBottomLength,
                          chestCircumferenceIn * widthPct)

        self.top = Shape.makeBlock(self)
        self.top.setup(chestCircumferenceIn * upperHeightPct,
                       chestCircumferenceIn * (widthPct - (2.0 * armpitDecreasePct)),
                       chestCircumferenceIn * neckWidthPct)

    def printInstructions(self, name, instructions):
        self.add_instruction(instructions, f"{name} panel:")
        runningRC = 0
        if self.bottomRibbing:
            self.bottomRibbing.printCastOn(instructions, "for 1x1 ribbing")
            runningRC = self.bottomRibbing.printInstructions(instructions, runningRC)
            self.add_instruction(instructions, "Now for the stockinette section")
        else:
            self.bottom.printCastOn(instructions)

        runningRC = self.bottom.printInstructions(instructions, runningRC)
        self.add_instruction(instructions, f"Cast off {self.convertWidth(self.armpitDecreasePct * self.chestCircumference)} on each side")
        self.top.printInstructions(instructions, runningRC)

    def printHalfInstructions(self, side, instructions, name="front"):
        self.add_instruction(instructions, f"Cardigan {name} {side} side:")
        runningRC = 0
        if self.bottomRibbing:
            self.bottomRibbing.printHalfCastOn(instructions, "for 1x1 ribbing")
            runningRC = self.bottomRibbing.printHalfInstructions(instructions, runningRC)
            self.add_instruction(instructions, "Now for the stockinette section")
        else:
            self.bottom.printHalfCastOn(instructions)

        runningRC = self.bottom.printHalfInstructions(instructions, runningRC, side=side)
        self.add_instruction(instructions, f"Cast off {self.convertWidth(self.armpitDecreasePct * self.chestCircumference)} on each side")
        self.top.printHalfInstructions(instructions, runningRC, side=side)

