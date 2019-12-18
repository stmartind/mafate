class Expe(object):

    def __init__(self, project, model, name, number=1, ybeg=1850, yend=1850, is_Obs=False, expe_control=None, label_plot='-', color='k', marker='.', linestyle='-',  adds=dict(), realization='i1p1*'):    
        self.project = project # CLIMAF project name (pre-existing or user)
        self.model = model
        self.name = name
        self.ybeg = ybeg
        self.yend = yend
        self.is_Obs = is_Obs
        if expe_control is None:
            self.expe_control = self
        else:
            self.expe_control = expe_control
        self.label_plot = label_plot
        self.color = color
        self.marker = marker
        self.linestyle = linestyle
        self.adds = adds
        self.number = number
        self.realization = realization
        
    def __str__(self):
        xstr = '---------------------------------------------------'
        xstr += '\n'
        xstr += 'Model  : %s'%(self.model)
        xstr += '\n'
        xstr += 'Name   : %s'%(self.name)
        xstr += '\n'
        xstr += 'Period : %i - %i'%(self.ybeg, self.yend)
        return xstr

    def period(self, norm=False, reftime=None):
        if reftime is None:
            reftime = self.ybeg
        if self.ybeg == 'fx':
            return 'fx'
        else:
            y1, y2 = reftime, reftime + self.yend - self.ybeg
            if norm:
                return str(y1).zfill(4)+'-'+str(y2).zfill(4)
            else:
                return str(y1)+'-'+str(y2)

    def expid(self):
        if self.is_Obs:
            return str(self.model)
        else:
            return str(self.model)+'_'+str(self.name)+'_r'+str(self.number)


class Variable(object):

    def __init__(self, name=None, table=None, grid='gr'):
        self.name = name
        self.table = table
        self.grid = grid

    def varid(self):
        return str(self.name)
#        return str(self.name)+'_'+str(self.table)

    def __str__(self):
        xstr = '---------------------------------------------------'
        xstr += '\n'
        xstr += 'name   : %s'%(self.name)
        xstr += '\n'
        xstr += 'table  : %s'%(self.table)
        xstr += '\n'
        xstr += 'grid   : %s'%(self.grid)
        return xstr        
