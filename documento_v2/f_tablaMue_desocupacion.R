f_tablaMue_desocupacion <- function(df_parametrostablas, str_region, cve, m){
  temp <-  df_parametrostablas %>% filter(Agregacion == str_region) 
  
  N <- temp$N
  M <- temp$M
  P = temp$P
  #cve <- temp$cve
  conf <- temp$conf
  r1 <- temp$r1
  r2 <- temp$r2
  b <-  temp$b  # Personas por hogar
  deff <- temp$deff
  
  nro_vivXUPM <- temp$nro_vivXUPM
  PM <- temp$PM # Perdida de Muestra
  TR <- temp$TR # Tasa de resupesta
  
  # Calculamos alpha, z, icc
  r <- r1  * r2 # Tasa de población afectada (dado que es un parámetro a nivel de persona)
  nbarra_encuesta <- nro_vivXUPM * b * r # Personas
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
  
  # Aumenta el número de hogares por UPM
  tabla_mue$HouseholdsPerPSU_Adjusted = ceiling(tabla_mue$HouseholdsPerPSU  /  ((1-PM) * TR))
  
  # Ya que informante idoneo es un miembro del hogar
  tabla_mue$HouseholdsInSample_Adjusted <- tabla_mue$HouseholdsPerPSU_Adjusted * 
    tabla_mue$PSUinSample 
  tabla_mue$PersonsInSample_Adjusted <- round(tabla_mue$HouseholdsInSample_Adjusted *  b * r) 
  
  tabla_mue$ajuste_perdida <- ((1-PM) * TR)
  tabla_mue$n_personaXhogar <- b * r
  tabla_mue$cve <- cve
  
  tabla_mue$M <- M
  tabla_mue$N <- N
  
  tabla_mue <- tabla_mue %>% relocate(cve)
  tabla_mue <- tabla_mue %>% relocate(n_personaXhogar)
  tabla_mue <- tabla_mue %>% relocate(ajuste_perdida)
  
  tabla_mue <- tabla_mue %>% relocate(M)
  tabla_mue <- tabla_mue %>% relocate(N)
  tabla_mue
}
