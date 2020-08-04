import sys
import os


def transmitFileUVCmd(maPath,uvPath,logPath,openLog=False,longName=True):
    '''
    after used 'transmitFileUVBackStage'
    '''
    import maya.cmds as cmds
    # open  ma file
    cmds.file(maPath, force=True, open=True, prompt=False,ignoreVersion=True)
    # reference UV
    filename = os.path.basename(uvPath)
    ns = os.path.splitext(filename)[0]
    refPath = cmds.file(uvPath, reference=True, ignoreVersion=True,
                        groupLocator=True, mergeNamespacesOnClash=False, 
                        options="v=0;",namespace=ns)
    
    allReferenceMesh = cmds.ls(type="mesh",referencedNodes=True,dag=True)
    allRefObj = [cmds.listRelatives(m,p=True,fullPath=True)[0] for m in allReferenceMesh if not cmds.getAttr("%s.intermediateObject"%m)]

    namespace = cmds.referenceQuery(refPath, namespace=True)
    namespace = namespace.lstrip(':')
    # passing data
    for uvObj in allRefObj:
        obj = uvObj.replace('|%s:'%namespace,'|')
        # obj:  "|mesh"
        obj = obj[1:]
        if not longName:
            obj = obj.rsplit('|',1)[0]
        
        if cmds.objExists(obj):
            transmit=uvObj
            receive=obj
            
            print [transmit,receive]
            # transmit uv 
            if cmds.listRelatives(receive): # judge the object if is None
                cmds.polyTransfer(receive,
                                  uv=1,
                                  ch=0,
                                  ao=transmit,
                                  constructionHistory=False)
    
    # remove reference
    cmds.file(refPath, removeReference=True)
    # save       
    cmds.file(force=True, save=True, prompt=False)



def main(argv):
    
    #print "argv:",argv
    #['D:/project/THHJ/assets/Ch/Jiaolong/rig/publish/v002/Jiaolong.ma',
    # 'D:/project/THHJ/assets/Ch/Jiaolong/tex/publish/v001/Jiaolong.abc',
    # 'C:/Users/wuxingcan/Desktop/Jiaolong_uvLog.txt',
    # 'True'
    # 'True']
    
    maPath,uvPath,logPath,openLog,longName = argv
    
    if openLog == 'True':
        openLog = True
    else:
        openLog = False
    
    if longName == 'True':
        longName = True
    else:
        longName = False
        
    
    if logPath:
        import traceback
        
        try:
            transmitFileUVCmd(maPath,uvPath,logPath,openLog,longName)
        except Exception, e:
            error = traceback.format_exc()
            
            logDir = os.path.dirname(logPath)
            if not os.path.exists(logDir):
                os.makedirs(logDir)
                
            with open(logPath,'w') as f:
                f.write(error)
        
            if openLog:
                os.startfile(logPath)
        
    else:
        transmitFileUVCmd(maPath,uvPath,logPath,openLog,longName)
    
    