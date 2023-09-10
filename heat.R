library(corrplot)

dt <- read.csv("E:2022_EastSea/BCvsMeteo_YS.csv")
M <- cor(dt,method='pearson')
testRes <- cor.mtest(dt, conf.level = 0.95)

windowsFonts()
par(family='TNM')

corrplot(M,p.mat =testRes$p,method ='color',
         sig.level = c( 0.01, 0.05), 
         # **:0.01, *:0.05
         insig='label_sig',pch.col = 'black',pch.cex=2,
         tl.col = 'black',type = 'upper',tl.pos = 'tp')

corrplot(M,p.mat=testRes$p, method = 'number', add=TRUE, 
         insig='n',col='black',number.cex =1.5,tl.cex=1,
         diag=FALSE,tl.col='black',type='lower',tl.pos = 'n',cl.pos = 'n')


