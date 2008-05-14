#!/usr/bin/env python
"""Keywords returned by tcamera, the TripleSpec Guider.

Notes:
- Keywords used only by the tcam actor are omitted.
- The slit keywords are in TSpecModel even though they are controlled by the TCamera actor.
This is because logically I consider the slit part of the spectrograph, not the guider.

2008-05-14 ROwen
"""
__all__ = ['getModel']

import RO.CnvUtil
import RO.KeyVariable
import TUI.TUIModel
import TUI.Inst.TSpec.TSpecCommonModel

_model = None

def getModel():
    global _model
    if _model == None:
        _model = Model()
    return _model

class Model (TUI.Inst.TSpec.TSpecCommonModel.TSpecCommonModel):
    def __init__(self):
        TUI.Inst.TSpec.TSpecCommonModel.TSpecCommonModel.__init__(self, "tcamera")

        keyVarFact = RO.KeyVariable.KeyVarFactory(
            actor = self.actor,
            dispatcher = self.dispatcher,
            converters = str,
            allowRefresh = True,
        )
        
        keyVarFact.setKeysRefreshCmd()


if __name__ == "__main__":
    getModel()
