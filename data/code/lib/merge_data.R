a <- matrix(
  c(1, 0, 0, 0)
  )

sigma_inv <- matrix(
    c(0.1, 1, 1, 1,
      1  , 2, 1, 1,
      1  , 1, 3, 1, 
      1  , 1, 1, 4), 
    nrow = 4, 
    byrow = T
  )

t(a) %*% sigma_inv %*% a


print(solve(sigma_inv))