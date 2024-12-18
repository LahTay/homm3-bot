"""Script containing building objects for every city"""

from data.building import *

#Castle
Castle_Tavern = Tavern("Tavern",360,530,1100,200,False,Cost(500,5,0,0,0,0,0))
Castle_Fort = Fort(0,"Fort",1400,300,800,200,False,(Cost(5000,20,20,0,0,0,0),Cost(2500,0,5,0,0,0,0),Cost(5000,10,10,0,0,0,0)))
Castle_Mage_Guild = MageGuild(0,"Mage_Guild", Spells("Placeholder"),(Cost(2000,5,5,0,0,0,0),Cost(1000,5,5,4,4,4,4),Cost(1000,5,5,6,6,6,6),Cost(1000,5,5,8,8,8,8),Cost(1000,5,5,10,10,10,10)),
                              x=1550,y=440,x2=850,y2=300,built=False)
Castle_City_Hall = CityHall(0,"City_Hall",500,500,500,200,True,(Cost(2500,0,0,0,0,0,0),Cost(5000,0,0,0,0,0,0),Cost(10000,0,0,0,0,0,0)))
Castle_Marketplace = Marketplace("Marketplace",1170,550,530,300,False,Cost(500,5,0,0,0,0,0))
Castle_Blacksmith = Building("Blacksmith",800,600,1400,200,False,Cost(1000,5,0,0,0,0,0))
Castle_Rescource_Silo= ResourceSilo("Resource_Silo",0,0,530,300,False,Cost(5000,0,5,0,0,0,0),income=Cost(0,1,1,0,0,0,0))#X1 i Y1 nie licza sie
#Castle unique buildings
Stables = Building("Stables",0,0,800,500,False,Cost(2000,10,0,0,0,0,0))#X1 i Y1 nie licza sie
Griffin_Bastion = Building("Griffin_Bastion",0,0,1100,500,False,Cost(1000,0,0,0,0,0,0))#X1 i Y1 nie licza sie
Brotherhood_of_the_Sword = Building("Brotherhood_of_the_Sword",0,0,1100,200,False,Cost(500,5,0,0,0,0,0))#X1 i Y1 nie licza sie
Lighthouse = Building("Lighthouse",0,0,0,0,False,Cost(2000,0,10,0,0,0,0))#X1 i Y1 nie licza sie


#Rampart
Rampart_Tavern = Tavern("Tavern",750,500,1100,200,False,Cost(500,5,0,0,0,0,0))
Rampart_Fort = Fort(0,"Fort",670,200,800,200,False,(Cost(5000,20,20,0,0,0,0),Cost(2500,0,5,0,0,0,0),Cost(5000,10,10,0,0,0,0)))
Rampart_Mage_Guild = MageGuild(0,"Mage_Guild",Spells("Placeholder"),(Cost(2000,5,5,0,0,0,0),Cost(1000,5,5,4,4,4,4),Cost(1000,5,5,6,6,6,6),Cost(1000,5,5,8,8,8,8),Cost(1000,5,5,10,10,10,10)),
                              1200,500,850,300,False)
Rampart_City_Hall = CityHall(0,"City_Hall",1400,500,500,200,True,(Cost(2500,0,0,0,0,0,0),Cost(5000,0,0,0,0,0,0),Cost(10000,0,0,0,0,0,0)))
Rampart_Marketplace = Marketplace("Marketplace",660,580,530,300,False,Cost(500,5,0,0,0,0,0))
Rampart_Blacksmith = Building("Blacksmith",1360,300,1400,200,False,Cost(1000,5,0,0,0,0,0))
Rampart_Rescource_Silo= ResourceSilo("Resource_Silo",0,0,530,300,False,Cost(5000,0,5,0,0,0,0),income=Cost(0,0,0,0,0,1,0))#X1 i Y1 nie licza sie
#Rampart unique buildings
Dendroid_Saplings = Building("Dendroid_Saplings",0,0,950,500,False,Cost(2000,0,0,0,0,0,0))#X1 i Y1 nie licza sie
Treasury = Building("Treasury",0,0,650,500,False,Cost(5000,5,10,0,0,0,0))#X1 i Y1 nie licza sie
Fountain_of_Fortune = Building("Fountain_of_Fortune",0,0,0,0,False,Cost(1500,0,0,0,0,10,0))#X1 i Y1 nie licza sie
Miners_Guild = Building("Miners_Guild",0,0,1250,500,False,Cost(1000,0,0,0,0,0,0))#X1 i Y1 nie licza sie
Mystic_Pond = Building("Mystic_Pond",0,0,1250,300,False,Cost(2000,2,2,2,2,2,2))#X1 i Y1 nie licza sie


#Tower
Tower_Tavern = Tavern("Tavern",1000,600,1100,200,False,Cost(500,5,0,0,0,0,0))
Tower_Fort = Fort(0,"Fort",930,400,800,200,False,(Cost(5000,20,20,0,0,0,0),Cost(2500,0,5,0,0,0,0),Cost(5000,10,10,0,0,0,0)))
Tower_Mage_Guild = MageGuild(0,"Mage_Guild",Spells("Placeholder"),(Cost(2000,5,5,0,0,0,0),Cost(1000,5,5,4,4,4,4),Cost(1000,5,5,6,6,6,6),Cost(1000,5,5,8,8,8,8),Cost(1000,5,5,10,10,10,10)),
                              1410,300,850,300,False)
Tower_City_Hall = CityHall(0,"City_Hall",450,550,500,200,True,(Cost(2500,0,0,0,0,0,0),Cost(5000,0,0,0,0,0,0),Cost(10000,0,0,0,0,0,0)))
Tower_Marketplace = Marketplace("Marketplace",1380,570,530,300,False,Cost(500,5,0,0,0,0,0))
Tower_Blacksmith = Building("Blacksmith",1200,570,1400,200,False,Cost(1000,5,0,0,0,0,0))
Tower_Rescource_Silo= ResourceSilo("Resource_Silo",0,0,530,300,False,Cost(5000,0,5,0,0,0,0),income=Cost(0,0,0,0,0,0,1))#X1 i Y1 nie licza sie
#Tower unique buildings
Artifact_Merchants_T = Building("Artifact_Merchants",1450,570,650,500,False,Cost(10000,0,0,0,0,0,0))
Library = Building("Library",0,0,1100,300,False,Cost(1500,5,5,5,5,5,5))#X1 i Y1 nie licza sie
Lookout_Tower = Building("Lookout_Tower",0,0,950,500,False,Cost(1000,5,0,0,0,0,0))#X1 i Y1 nie licza sie
Sculptor_Wings = Building("Sculptor_Wings",0,0,1250,500,False,Cost(1000,0,0,0,0,0,0))#X1 i Y1 nie licza sie
Wall_of_Knowledge = Building("Wall_of_Knowledge",0,0,1400,300,False,Cost(1000,0,5,0,0,0,0))#X1 i Y1 nie licza sie


#Inferno
Inferno_Tavern = Tavern("Tavern",550,480,1100,200,False,Cost(500,5,0,0,0,0,0))
Inferno_Fort = Fort(0,"Fort",900,400,800,200,False,(Cost(5000,20,20,0,0,0,0),Cost(2500,0,5,0,0,0,0),Cost(5000,10,10,0,0,0,0)))
Inferno_Mage_Guild = MageGuild(0,"Mage_Guild",Spells("Placeholder"),(Cost(2000,5,5,0,0,0,0),Cost(1000,5,5,4,4,4,4),Cost(1000,5,5,6,6,6,6),Cost(1000,5,5,8,8,8,8),Cost(1000,5,5,10,10,10,10)),
                              1500,380,850,300,False)
Inferno_City_Hall = CityHall(0,"City_Hall",450,400,500,200,True,(Cost(2500,0,0,0,0,0,0),Cost(5000,0,0,0,0,0,0),Cost(10000,0,0,0,0,0,0)))
Inferno_Marketplace = Marketplace("Marketplace",1250,600,530,300,False,Cost(500,5,0,0,0,0,0))
Inferno_Blacksmith = Building("Blacksmith",1530,600,1400,200,False,Cost(1000,5,0,0,0,0,0))
Inferno_Rescource_Silo= ResourceSilo("Resource_Silo",0,0,530,300,False,Cost(5000,0,5,0,0,0,0),income=Cost(0,0,0,1,0,0,0))#X1 i Y1 nie licza sie
#Inferno unique buildings
Order_of_Fire = Building("Order_of_Fire",0,0,1100,300,False,Cost(1000,5,0,0,0,0,0))#X1 i Y1 nie licza sie
Castle_Gate = Building("Castle_Gate",735,370,650,500,False,Cost(10000,5,5,0,0,0,500))
Cages = Building("Cages",0,0,1250,500,False,Cost(1000,0,0,0,0,0,0))#X1 i Y1 nie licza sie
Brimstone_Stormclouds = Building("Brimstone_Stormclouds",0,0,1400,300,False,Cost(1000,0,0,0,4,0,0))#X1 i Y1 nie licza sie
Birthing_Pools = Building("Birthing_Pools",0,0,950,500,False,Cost(1000,0,0,0,0,0,0))#X1 i Y1 nie licza sie


#Necropolis
Necropolis_Tavern = Tavern("Tavern",1300,400,1100,200,False,Cost(500,5,0,0,0,0,0))
Necropolis_Fort = Fort(0,"Fort",760,250,800,200,False,(Cost(5000,20,20,0,0,0,0),Cost(2500,0,5,0,0,0,0),Cost(5000,10,10,0,0,0,0)))
Necropolis_Mage_Guild = MageGuild(0,"Mage_Guild",Spells("Placeholder"),(Cost(2000,5,5,0,0,0,0),Cost(1000,5,5,4,4,4,4),Cost(1000,5,5,6,6,6,6),Cost(1000,5,5,8,8,8,8),Cost(1000,5,5,10,10,10,10)),
                              990,280,850,300,False)
Necropolis_City_Hall = CityHall(0,"City_Hall",1200,300,500,200,True,(Cost(2500,0,0,0,0,0,0),Cost(5000,0,0,0,0,0,0),Cost(10000,0,0,0,0,0,0)))
Necropolis_Marketplace = Marketplace("Marketplace",980,440,530,300,False,Cost(500,5,0,0,0,0,0))
Necropolis_Blacksmith = Building("Blacksmith",1000,500,1400,200,False,Cost(1000,5,0,0,0,0,0))
Necropolis_Rescource_Silo= ResourceSilo("Resource_Silo",0,0,530,300,False,Cost(5000,0,5,0,0,0,0),income=Cost(0,1,1,0,0,0,0))#X1 i Y1 nie licza sie
#Necropolis unique buildings
Necromancy_Amplifier = Building("Necromancy_Amplifier",0,0,1100,350,False,Cost(1000,0,0,0,0,0,0))#X1 i Y1 nie licza sie
Cover_of_Darkness = Building("Cover_of_Darkness",0,0,950,500,False,Cost(1000,0,0,0,0,0,0))#X1 i Y1 nie licza sie
Skeleton_Transformer = Building("Skeleton_Transformer",790,530,950,500,False,Cost(1000,0,0,0,0,0,0))
Unearthed_Graves = Building("Unearthed_Graves",0,0,1250,500,False,Cost(1000,0,0,0,0,0,0))#X1 i Y1 nie licza sie


#Dungeon
Dungeon_Tavern = Tavern("Tavern",700,600,1100,200,False,Cost(500,5,0,0,0,0,0))
Dungeon_Fort = Fort(0,"Fort",1050,350,800,200,False,(Cost(5000,20,20,0,0,0,0),Cost(2500,0,5,0,0,0,0),Cost(5000,10,10,0,0,0,0)))
Dungeon_Mage_Guild = MageGuild(0,"Mage_Guild",Spells("Placeholder"),(Cost(2000,5,5,0,0,0,0),Cost(1000,5,5,4,4,4,4),Cost(1000,5,5,6,6,6,6),Cost(1000,5,5,8,8,8,8),Cost(1000,5,5,10,10,10,10)),
                              650,330,850,300,False)
Dungeon_City_Hall = CityHall(0,"City_Hall",450,490,500,200,True,(Cost(2500,0,0,0,0,0,0),Cost(5000,0,0,0,0,0,0),Cost(10000,0,0,0,0,0,0)))
Dungeon_Marketplace = Marketplace("Marketplace",1420,645,530,300,False,Cost(500,5,0,0,0,0,0))
Dungeon_Blacksmith = Building("Blacksmith",1250,550,1400,200,False,Cost(1000,5,0,0,0,0,0))
Dungeon_Rescource_Silo= ResourceSilo("Resource_Silo",0,0,530,300,False,Cost(5000,0,5,0,0,0,0),income=Cost(0,0,0,0,1,0,0))#X1 i Y1 nie licza sie
#Dungeon unique buildings
Artifact_Merchants_D = Building("Artifact_Merchants_D",1570,580,650,500,False,Cost(10000,0,0,0,0,0,0))
Portal_of_Summoning = Building("Portal_of_Summoning",1520,420,1400,300,False,Cost(2500,0,5,0,0,0,0))
Mana_Vortex = Building("Mana_Vortex",0,0,1100,300,False,Cost(1000,0,0,0,0,0,0))#X1 i Y1 nie licza sie
Battle_Scholar_Academy = Building("Battle_Scholar_Academy",0,0,950,500,False,Cost(1000,5,5,0,0,0,0))#X1 i Y1 nie licza sie
Mushroom_Rings = Building("Mushroom_Rings",0,0,1250,500,False,Cost(1000,0,0,0,0,0,0))#X1 i Y1 nie licza sie


#Stronghold
Stronghold_Tavern = Tavern("Tavern",730,560,1100,200,False,Cost(500,5,0,0,0,0,0))
Stronghold_Fort = Fort(0,"Fort",1100,370,800,200,False,(Cost(5000,20,20,0,0,0,0),Cost(2500,0,5,0,0,0,0),Cost(5000,10,10,0,0,0,0)))
Stronghold_Mage_Guild = MageGuild(0,"Mage_Guild",Spells("Placeholder"),(Cost(2000,5,5,0,0,0,0),Cost(1000,5,5,4,4,4,4),Cost(1000,5,5,6,6,6,6),Cost(1000,5,5,8,8,8,8),Cost(1000,5,5,10,10,10,10)),
                              1160,200,850,300,False)
Stronghold_City_Hall = CityHall(0,"City_Hall",500,570,500,200,True,(Cost(2500,0,0,0,0,0,0),Cost(5000,0,0,0,0,0,0),Cost(10000,0,0,0,0,0,0)))
Stronghold_Marketplace = Marketplace("Marketplace",1060,580,530,300,False,Cost(500,5,0,0,0,0,0))
Stronghold_Blacksmith = Building("Blacksmith",1460,600,1400,200,False,Cost(1000,5,0,0,0,0,0))
Stronghold_Rescource_Silo= ResourceSilo("Resource_Silo",0,0,530,300,False,Cost(5000,0,5,0,0,0,0),income=Cost(0,1,1,0,0,0,0))#X1 i Y1 nie licza sie
#Stronghold unique buildings
Ballista_Yard = Building("Ballista_Yard",1375,610,950,500,False,Cost(1000,5,0,0,0,0,0))
Freelancers_Guild = Building("Freelancers_Guild",1130,570,650,500,False,Cost(1000,0,0,0,0,0,0))
Mess_Hall = Building("Mess_Hall",0,0,1250,500,False,Cost(1000,0,0,0,0,0,0))#X1 i Y1 nie licza sie
Escape_Tunnel = Building("Escape_Tunnel",0,0,1400,300,False,Cost(2000,5,5,0,0,0,0))#X1 i Y1 nie licza sie
Hall_of_Valhalla = Building("Hall_of_Valhalla",0,0,1100,300,False,Cost(1000,0,0,0,0,0,0))#X1 i Y1 nie licza sie


#Fortress
Fortress_Tavern = Tavern("Tavern",1550,500,1100,200,False,Cost(500,5,0,0,0,0,0))
Fortress_Fort = Fort(0,"Fort",1200,350,800,200,False,(Cost(5000,20,20,0,0,0,0),Cost(2500,0,5,0,0,0,0),Cost(5000,10,10,0,0,0,0)))
Fortress_Mage_Guild = MageGuild(0,"Mage_Guild",Spells("Placeholder"),(Cost(2000,5,5,0,0,0,0),Cost(1000,5,5,4,4,4,4),Cost(1000,5,5,6,6,6,6),Cost(1000,5,5,8,8,8,8),Cost(1000,5,5,10,10,10,10)),
                              400,460,850,300,False)
Fortress_City_Hall = CityHall(0,"City_Hall",820,290,500,200,True,(Cost(2500,0,0,0,0,0,0),Cost(5000,0,0,0,0,0,0),Cost(10000,0,0,0,0,0,0)))
Fortress_Marketplace = Marketplace("Marketplace",1055,485,530,300,False,Cost(500,5,0,0,0,0,0))
Fortress_Blacksmith = Building("Blacksmith",980,380,1400,200,False,Cost(1000,5,0,0,0,0,0))
Fortress_Rescource_Silo= ResourceSilo("Resource_Silo",0,0,530,300,False,Cost(5000,0,5,0,0,0,0),income=Cost(0,1,1,0,0,0,0))#X1 i Y1 nie licza sie
#Fortress unique buildings
Blood_Obelisk = Building("Blood_Obelisk",0,0,950,500,False,Cost(1000,0,0,0,0,0,0))#X1 i Y1 nie licza sie
Cage_of_Warlords = Building("Cage_of_Warlords",0,0,650,500,False,Cost(1000,0,0,0,0,0,0))#X1 i Y1 nie licza sie
Captains_Quarters = Building("Captains_Quarters",0,0,1250,500,False,Cost(1000,0,0,0,0,0,0))#X1 i Y1 nie licza sie
Glyphs_of_Fear = Building("Glyphs_of_Fear",0,0,950,500,False,Cost(1000,0,0,0,0,0,0))#X1 i Y1 nie licza sie


#Conflux
Conflux_Tavern = Tavern("Tavern",1280,470,1100,200,False,Cost(500,5,0,0,0,0,0))
Conflux_Fort = Fort(0,"Fort",1300,380,800,200,False,(Cost(5000,20,20,0,0,0,0),Cost(2500,0,5,0,0,0,0),Cost(5000,10,10,0,0,0,0)))
Conflux_Mage_Guild = MageGuild(0,"Mage_Guild",Spells("Placeholder"),(Cost(2000,5,5,0,0,0,0),Cost(1000,5,5,4,4,4,4),Cost(1000,5,5,6,6,6,6),Cost(1000,5,5,8,8,8,8),Cost(1000,5,5,10,10,10,10)),
                              730,470,850,300,False)
Conflux_City_Hall = CityHall(0,"City_Hall",500,530,500,200,True,(Cost(2500,0,0,0,0,0,0),Cost(5000,0,0,0,0,0,0),Cost(10000,0,0,0,0,0,0)))
Conflux_Marketplace = Marketplace("Marketplace",940,500,530,300,False,Cost(500,5,0,0,0,0,0))
Conflux_Blacksmith = Building("Blacksmith",1100,430,1400,200,False,Cost(1000,5,0,0,0,0,0))
Conflux_Rescource_Silo= ResourceSilo("Resource_Silo",0,0,530,300,False,Cost(5000,0,5,0,0,0,0),income=Cost(0,0,0,1,0,0,0))#X1 i Y1 nie licza sie
#Conflux unique buildings
Magic_University = Building("Magic_University",630,430,1100,300,False,Cost(5000,10,10,0,0,0,0))
Artifact_Merchants_C = Building("Artifact_Merchants_C",840,520,650,500,False,Cost(10000,0,0,0,0,0,0))
Garden_of_Life = Building("Garden_of_Life",0,0,1250,500,False,Cost(1000,0,0,0,0,0,0))#X1 i Y1 nie licza sie
Vault_of_Ashes = Building("Vault_of_Ashes",0,0,950,500,False,Cost(5000,0,0,5,0,0,0))#X1 i Y1 nie licza sie


#Cove
Cove_Tavern = Tavern("Tavern",420,580,1100,200,False,Cost(500,5,0,0,0,0,0))
Cove_Fort = Fort(0,"Fort",1200,350,800,200,False,(Cost(5000,20,20,0,0,0,0),Cost(2500,0,5,0,0,0,0),Cost(5000,10,10,0,0,0,0)))
Cove_Mage_Guild = MageGuild(0,"Mage_Guild",Spells("Placeholder"),(Cost(2000,5,5,0,0,0,0),Cost(1000,5,5,4,4,4,4),Cost(1000,5,5,6,6,6,6),Cost(1000,5,5,8,8,8,8),Cost(1000,5,5,10,10,10,10)),
                              910,300,850,300,False)
Cove_City_Hall = CityHall(0,"City_Hall",520,400,500,200,True,(Cost(2500,0,0,0,0,0,0),Cost(5000,0,0,0,0,0,0),Cost(10000,0,0,0,0,0,0)))
Cove_Marketplace = Marketplace("Marketplace",950,600,530,300,False,Cost(500,5,0,0,0,0,0))
Cove_Blacksmith = Building("Blacksmith",1520,570,1400,200,False,Cost(1000,5,0,0,0,0,0))
Cove_Rescource_Silo= ResourceSilo("Resource_Silo",0,0,530,300,False,Cost(5000,0,5,0,0,0,0),income=Cost(0,0,0,0,1,0,0))#X1 i Y1 nie licza sie
#Cove unique buildings
Pub = Building("Pub",0,0,650,500,False,Cost(1000,0,0,0,0,0,0))#X1 i Y1 nie licza sie
Roost = Building("Roost",0,0,1250,500,False,Cost(1000,0,0,0,0,0,0))#X1 i Y1 nie licza sie
Grotto = Building("Grotto",780,410,950,500,False,Cost(7500,15,15,0,0,0,0))
Thieves_Guild  = Building("Thieves_Guild",350,240,1400,300,False,Cost(500,5,0,0,0,0,0))
