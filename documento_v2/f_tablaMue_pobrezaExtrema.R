f_tablaMue_PobrezaExtrema <- function(df_parametrostablas, str_region, cve, m){
  temp <-  df_parametrostablas %>% filter(Agregacion == str_region) 
  
  N <- temp$N
  M <- temp$M
  P = temp$P
  #cve <- temp$cve
  conf <- temp$conf
  r <- temp$r
  
  b <-  temp$b  # Personas por hogar
  deff <- temp$deff
  
  PM <- temp$PM # Perdida de Muestra
  TR <- temp$TR # Tasa de resupesta
  
  # Calculamos alpha, z, icc
  nbarra_encuesta <- temp$nro_vivXUPM # Personas
  alpha <- 1 - conf
  z <- qnorm(1-alpha/2)
  icc <- (deff - 1) / (nbarra_encuesta - 1) 
  
  # Tabla de muestreo 
  tabla_mue <- ss4HHSp(N,
                       M, # Recuendo no poderado
                       r,  # tasa que afecta
                       b, 
                       rho = icc,
                       P, 
                       delta =  cve * z, #  Error estándar relativo,
                       conf, m = m)
  
  
  tabla_mue$HouseholdsPerPSU_Adjusted = ceiling(tabla_mue$HouseholdsPerPSU  /  ((1-PM) * TR))
  tabla_mue$HouseholdsInSample_Adjusted <- tabla_mue$HouseholdsPerPSU_Adjusted *  
    tabla_mue$PSUinSample 
  
  tabla_mue$ajuste_perdida <- ((1-PM) * TR)
  tabla_mue$M <- M
  tabla_mue$N <- N
  tabla_mue$cve <- cve
  
  tabla_mue <- tabla_mue %>% relocate(cve)
  tabla_mue <- tabla_mue %>% relocate(ajuste_perdida)
  tabla_mue <- tabla_mue %>% relocate(M)
  tabla_mue <- tabla_mue %>% relocate(N)
  tabla_mue
}
