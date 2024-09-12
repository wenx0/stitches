from base import Block, BodyPannel, Sleeve

class SetInSleeveSweater(Block):
    def setup(self, chestCircumferenceIn):
        self.front = BodyPannel.makeBlock(self)
        self.front.setup(chestCircumferenceIn)

        self.back = BodyPannel.makeBlock(self)
        self.back.setup(chestCircumferenceIn, neckWidthPct=0.1)

        self.sleeve = Sleeve.makeBlock(self)
        self.sleeve.setup(chestCircumferenceIn, lowerSleeveWidthPct=0.5, armpitDecreasePct=0.05, upperHeightPct=0.25)

    def printInstructions(self, instructions):
        self.sleeve.printInstructions(instructions)
        instructions.append("\n")
        self.back.printInstructions("Back", instructions)
        instructions.append("\n")
        self.front.printInstructions("Front", instructions)
