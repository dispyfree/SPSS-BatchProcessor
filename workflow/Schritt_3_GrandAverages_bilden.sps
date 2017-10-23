* Encoding: UTF-8.

*Fz.
GET FILE="\sav\Pbn_c_fair_Filter.sav".
select if (CASE_LBL="Fz").
execute.
SAVE OUTFILE='\sav\Pbn_c_fair_FilterFz.sav'
  /COMPRESSED.
FLIP VARIABLES=CASE_LBL var001 var002 var003 var004 var005 var006 var007 var008 var009 var010 var011 var012 var013 var014 
var015 var016 var017 var018 var019 var020 var021 var022 var023 var024 var025 var026 var027 var028 var029 var030 var031 var032 var033 
var034 var035 var036 var037 var038 var039 var040 var041 var042 var043 var044 var045 var046 var047 var048 var049 var050 var051 var052
 var053 var054 var055 var056 var057 var058 var059 var060 var061 var062 var063 var064 var065 var066 var067 var068 var069
var070 var071 var072 var073 var074 var075 var076 var077 var078 var079 var080 var081 var082 var083 var084 var085 var086 var087 var088 
var089 var090 var091 var092 var093 var094 var095 var096 var097 var098 var099 var100 var101 var102 var103 var104 var105 var106 var107 
var108 var109 var110 var111 var112 var113 var114 var115 var116 var117 var118 var119 var120 var121 var122 var123 var124 var125 var126 
var127 var128 var129 var130 var131 var132 var133 var134 var135 var136 var137 var138 var139 var140 var141 var142
var143 var144 var145 var146 var147 var148 var149 var150 var151 var152 var153 var154 var155 var156 var157 var158 var159 var160 var161 
var162 var163 var164 var165 var166 var167 var168 var169 var170 var171 var172 var173 var174 var175 var176 var177 var178 var179 var180 
var181 var182 var183 var184 var185 var186 var187 var188 var189 var190 var191 var192 var193 var194 var195 var196 var197 var198 var199 
var200 var201 var202 var203 var204 var205 var206 var207 var208 var209 var210 var211 var212 var213 var214 var215
var216 var217 var218 var219 var220 var221 var222 var223 var224 var225 var226 var227 var228 var229 var230 var231 var232 var233 var234 
var235 var236 var237 var238 var239 var240 var241 var242 var243 var244 var245 var246 var247 var248 var249 var250 var251 var252 var253 
var254 var255 var256 var257 var258 var259 var260 var261 var262 var263 var264 var265 var266 var267 var268 var269 var270 var271 var272 
var273 var274 var275 var276 var277 var278 var279 var280 var281 var282 var283 var284 var285 var286 var287 var288
var289 var290 var291 var292 var293 var294 var295 var296 var297 var298 var299 var300 var301 var302 var303 var304 var305 var306 var307 
var308 var309 var310 var311 var312 var313 var314 var315 var316 var317 var318 var319 var320 var321 var322 var323 var324 var325 var326 
var327 var328 var329 var330 var331 var332 var333 var334 var335 var336 var337 var338 var339 var340 var341 var342 var343 var344 var345 
var346 var347 var348 var349 var350 var351 var352 var353 var354 var355 var356 var357 var358 var359 var360 var361
var362 var363 var364 var365 var366 var367 var368 var369 var370 var371 var372 var373 var374 var375 var376 var377 var378 var379 var380 
var381 var382 var383 var384 var385 var386 var387 var388 var389 var390 var391 var392 var393 var394 var395 var396 var397 var398 var399 
var400 var401 var402 var403 var404 var405 var406 var407 var408 var409 var410 var411 var412 var413 var414 
var415 var416 var417 var418 var419 var420 var421 var422 var423 var424 var425 var426 var427 var428 var429 var430 var431 var432 var433 
var434 var435 var436 var437 var438 var439 var440 var441 var442 var443 var444 var445 var446 var447 var448 var449 var450 var451 var452
 var453 var454 var455 var456 var457 var458 var459 var460 var461 var462 var463 var464 var465 var466 var467 var468 var469
var470 var471 var472 var473 var474 var475 var476 var477 var478 var479 var480 var481 var482 var483 var484 var485 var486 var487 var488 
var489 var490 var491 var492 var493 var494 var495 var496 var497 var498 var499 var500 var501 var502 var503 var504 var505 var506 var507 
var508 var509 var510 var511 var512 var513 var514 var515 var516 var517 var518 var519 var520 var521 var522 var523 var524 var525 var526 
var527 var528 var529 var530 var531 var532 var533 var534 var535 var536 var537 var538 var539 var540 var541 var542
var543 var544 var545 var546 var547 var548 var549 var550 var551 var552 var553 var554 var555 var556 var557 var558 var559 var560 var561 
var562 var563.
SAVE OUTFILE='Pbn_c_fair_FilterFz_t.sav'
  /COMPRESSED.
compute fz_fair=mean(Fz to Fz_AA).
execute.
SAVE OUTFILE='\sav\Pbn_c_fair_FilterFz_tt.sav'
  /COMPRESSED.


*Cz.
GET FILE="sav\Pbn_c_fair_Filter.sav".
select if (CASE_LBL="Cz").
execute.
SAVE OUTFILE='sav\Pbn_c_fair_FilterCz.sav'
  /COMPRESSED.
FLIP VARIABLES=CASE_LBL var001 var002 var003 var004 var005 var006 var007 var008 var009 var010 var011 var012 var013 var014 
var015 var016 var017 var018 var019 var020 var021 var022 var023 var024 var025 var026 var027 var028 var029 var030 var031 var032 var033 
var034 var035 var036 var037 var038 var039 var040 var041 var042 var043 var044 var045 var046 var047 var048 var049 var050 var051 var052
 var053 var054 var055 var056 var057 var058 var059 var060 var061 var062 var063 var064 var065 var066 var067 var068 var069
var070 var071 var072 var073 var074 var075 var076 var077 var078 var079 var080 var081 var082 var083 var084 var085 var086 var087 var088 
var089 var090 var091 var092 var093 var094 var095 var096 var097 var098 var099 var100 var101 var102 var103 var104 var105 var106 var107 
var108 var109 var110 var111 var112 var113 var114 var115 var116 var117 var118 var119 var120 var121 var122 var123 var124 var125 var126 
var127 var128 var129 var130 var131 var132 var133 var134 var135 var136 var137 var138 var139 var140 var141 var142
var143 var144 var145 var146 var147 var148 var149 var150 var151 var152 var153 var154 var155 var156 var157 var158 var159 var160 var161 
var162 var163 var164 var165 var166 var167 var168 var169 var170 var171 var172 var173 var174 var175 var176 var177 var178 var179 var180 
var181 var182 var183 var184 var185 var186 var187 var188 var189 var190 var191 var192 var193 var194 var195 var196 var197 var198 var199 
var200 var201 var202 var203 var204 var205 var206 var207 var208 var209 var210 var211 var212 var213 var214 var215
var216 var217 var218 var219 var220 var221 var222 var223 var224 var225 var226 var227 var228 var229 var230 var231 var232 var233 var234 
var235 var236 var237 var238 var239 var240 var241 var242 var243 var244 var245 var246 var247 var248 var249 var250 var251 var252 var253 
var254 var255 var256 var257 var258 var259 var260 var261 var262 var263 var264 var265 var266 var267 var268 var269 var270 var271 var272 
var273 var274 var275 var276 var277 var278 var279 var280 var281 var282 var283 var284 var285 var286 var287 var288
var289 var290 var291 var292 var293 var294 var295 var296 var297 var298 var299 var300 var301 var302 var303 var304 var305 var306 var307 
var308 var309 var310 var311 var312 var313 var314 var315 var316 var317 var318 var319 var320 var321 var322 var323 var324 var325 var326 
var327 var328 var329 var330 var331 var332 var333 var334 var335 var336 var337 var338 var339 var340 var341 var342 var343 var344 var345 
var346 var347 var348 var349 var350 var351 var352 var353 var354 var355 var356 var357 var358 var359 var360 var361
var362 var363 var364 var365 var366 var367 var368 var369 var370 var371 var372 var373 var374 var375 var376 var377 var378 var379 var380 
var381 var382 var383 var384 var385 var386 var387 var388 var389 var390 var391 var392 var393 var394 var395 var396 var397 var398 var399 
var400 var401 var402 var403 var404 var405 var406 var407 var408 var409 var410 var411 var412 var413 var414 
var415 var416 var417 var418 var419 var420 var421 var422 var423 var424 var425 var426 var427 var428 var429 var430 var431 var432 var433 
var434 var435 var436 var437 var438 var439 var440 var441 var442 var443 var444 var445 var446 var447 var448 var449 var450 var451 var452
 var453 var454 var455 var456 var457 var458 var459 var460 var461 var462 var463 var464 var465 var466 var467 var468 var469
var470 var471 var472 var473 var474 var475 var476 var477 var478 var479 var480 var481 var482 var483 var484 var485 var486 var487 var488 
var489 var490 var491 var492 var493 var494 var495 var496 var497 var498 var499 var500 var501 var502 var503 var504 var505 var506 var507 
var508 var509 var510 var511 var512 var513 var514 var515 var516 var517 var518 var519 var520 var521 var522 var523 var524 var525 var526 
var527 var528 var529 var530 var531 var532 var533 var534 var535 var536 var537 var538 var539 var540 var541 var542
var543 var544 var545 var546 var547 var548 var549 var550 var551 var552 var553 var554 var555 var556 var557 var558 var559 var560 var561 
var562 var563.
SAVE OUTFILE='Pbn_c_fair_FilterCz_t.sav'
  /COMPRESSED.
compute cz_fair=mean(Cz to Cz_AA).
execute.
SAVE OUTFILE='Pbn_c_fair_FilterCz_tt.sav'
  /COMPRESSED.

*Pz.
GET FILE="Pbn_c_fair_Filter.sav".
select if (CASE_LBL="Pz").
execute.
SAVE OUTFILE='Pbn_c_fair_FilterPz.sav'
  /COMPRESSED.
FLIP VARIABLES=CASE_LBL var001 var002 var003 var004 var005 var006 var007 var008 var009 var010 var011 var012 var013 var014 
var015 var016 var017 var018 var019 var020 var021 var022 var023 var024 var025 var026 var027 var028 var029 var030 var031 var032 var033 
var034 var035 var036 var037 var038 var039 var040 var041 var042 var043 var044 var045 var046 var047 var048 var049 var050 var051 var052
 var053 var054 var055 var056 var057 var058 var059 var060 var061 var062 var063 var064 var065 var066 var067 var068 var069
var070 var071 var072 var073 var074 var075 var076 var077 var078 var079 var080 var081 var082 var083 var084 var085 var086 var087 var088 
var089 var090 var091 var092 var093 var094 var095 var096 var097 var098 var099 var100 var101 var102 var103 var104 var105 var106 var107 
var108 var109 var110 var111 var112 var113 var114 var115 var116 var117 var118 var119 var120 var121 var122 var123 var124 var125 var126 
var127 var128 var129 var130 var131 var132 var133 var134 var135 var136 var137 var138 var139 var140 var141 var142
var143 var144 var145 var146 var147 var148 var149 var150 var151 var152 var153 var154 var155 var156 var157 var158 var159 var160 var161 
var162 var163 var164 var165 var166 var167 var168 var169 var170 var171 var172 var173 var174 var175 var176 var177 var178 var179 var180 
var181 var182 var183 var184 var185 var186 var187 var188 var189 var190 var191 var192 var193 var194 var195 var196 var197 var198 var199 
var200 var201 var202 var203 var204 var205 var206 var207 var208 var209 var210 var211 var212 var213 var214 var215
var216 var217 var218 var219 var220 var221 var222 var223 var224 var225 var226 var227 var228 var229 var230 var231 var232 var233 var234 
var235 var236 var237 var238 var239 var240 var241 var242 var243 var244 var245 var246 var247 var248 var249 var250 var251 var252 var253 
var254 var255 var256 var257 var258 var259 var260 var261 var262 var263 var264 var265 var266 var267 var268 var269 var270 var271 var272 
var273 var274 var275 var276 var277 var278 var279 var280 var281 var282 var283 var284 var285 var286 var287 var288
var289 var290 var291 var292 var293 var294 var295 var296 var297 var298 var299 var300 var301 var302 var303 var304 var305 var306 var307 
var308 var309 var310 var311 var312 var313 var314 var315 var316 var317 var318 var319 var320 var321 var322 var323 var324 var325 var326 
var327 var328 var329 var330 var331 var332 var333 var334 var335 var336 var337 var338 var339 var340 var341 var342 var343 var344 var345 
var346 var347 var348 var349 var350 var351 var352 var353 var354 var355 var356 var357 var358 var359 var360 var361
var362 var363 var364 var365 var366 var367 var368 var369 var370 var371 var372 var373 var374 var375 var376 var377 var378 var379 var380 
var381 var382 var383 var384 var385 var386 var387 var388 var389 var390 var391 var392 var393 var394 var395 var396 var397 var398 var399 
var400 var401 var402 var403 var404 var405 var406 var407 var408 var409 var410 var411 var412 var413 var414 
var415 var416 var417 var418 var419 var420 var421 var422 var423 var424 var425 var426 var427 var428 var429 var430 var431 var432 var433 
var434 var435 var436 var437 var438 var439 var440 var441 var442 var443 var444 var445 var446 var447 var448 var449 var450 var451 var452
 var453 var454 var455 var456 var457 var458 var459 var460 var461 var462 var463 var464 var465 var466 var467 var468 var469
var470 var471 var472 var473 var474 var475 var476 var477 var478 var479 var480 var481 var482 var483 var484 var485 var486 var487 var488 
var489 var490 var491 var492 var493 var494 var495 var496 var497 var498 var499 var500 var501 var502 var503 var504 var505 var506 var507 
var508 var509 var510 var511 var512 var513 var514 var515 var516 var517 var518 var519 var520 var521 var522 var523 var524 var525 var526 
var527 var528 var529 var530 var531 var532 var533 var534 var535 var536 var537 var538 var539 var540 var541 var542
var543 var544 var545 var546 var547 var548 var549 var550 var551 var552 var553 var554 var555 var556 var557 var558 var559 var560 var561 
var562 var563.
SAVE OUTFILE='Pbn_c_fair_FilterPz_t.sav'
  /COMPRESSED.
compute pz_fair=mean(Pz to Pz_AB).
execute.
SAVE OUTFILE='Pbn_c_fair_FilterPz_tt.sav'
  /COMPRESSED.

