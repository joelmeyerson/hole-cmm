A short Python script to generate a Chimera marker file (.cmm) using the output from the standalone version of HOLE or the Coot implementation of HOLE. The marker file can be opened in Chimera or ChimeraX to visualize the HOLE output. The script has options to customize coloring and sphere size.

[HOLE homepage](http://www.holeprogram.org/) <br />
[HOLE GitHub page](https://github.com/osmart/hole2) <br />
[HOLE in Coot](https://www2.mrc-lmb.cam.ac.uk/personal/pemsley/coot/web/docs/coot.html#Coot_0027s-Hole-implementation) <br />

### Running the script

`python holecmm.py -i <input> [-o <output> -r <marker radius> -c1 <hex color> -c2 <hex color> -c3 <hex color>]`
	
`-i` input file in .vmd_plot (HOLE) or .dat format (Coot HOLE) <br />
`-o` output file name (default is `hole.cmm`) <br />
`-r` radius of spheres that mark the HOLE surface (default is `0.2`) <br />
`-c1` color for pore radius less than 1.15 Å (default is `FF0000`) <br />
`-c2` color for pore radius between 1.15 Å and 2.30 Å (default is `00FF00`) <br />
`-c2` color for pore radius greater than 2.30 Å (default is `0000FF`) <br />

### Example using HOLE

This example uses the KcsA structure (PDB: 1BL8) but with the potassium ions removed.

1. Download HOLE.
2. Create a HOLE card with the input settings. These are the contents of `hole-kcsa.inp`. <br />
```
! Card for KcsA (1BL8) with potassium ions removed
coord 1bl8-no-K.pdb          	! Co-ordinates in pdb format
radius ~/hole2/rad/simple.rad	! Use simple AMBER vdw radii
sphpdb hole-kcsa.sph            ! pdb format output of hole sphere centre info
endrad 10.                      ! This is the pore radius that is taken as where the channel ends
```
3. Run HOLE. <br />
`hole < hole-kcsa.inp > hole-kcsa.log`
`sph_process -dotden 15 -color -nocen hole-kcsa.sph dotsurface-kcsa.qpt`
4. Run qpt_conv interactively to convert the .qpt file to a .vmd file. When prompted choose VMD format by entering `D` at the command line. Use defaults for the other prompts. The output file will be called `dotsurface-kcsa.vmd_plot'. <br />
`qpt_conv`
5. Run the holecmm.py script to generate a .cmm file. In this example custom colors are used for the different pore diameters. <br />
`python holecmm.py -i dotsurface-kcsa.vmd_plot -o kcsa.cmm -r 0.2 -c1 FF6347 -c2 90EE90 -c3 6495ED`

### Example using HOLE in Coot

This example uses the KcsA structure (PDB: 1BL8) but with the potassium ions removed.

1. Launch Coot and open the PDB file.
2. Open the HOLE dialog box from the menu. <br />
`Draw > Representation Tools... > HOLE...`
3. Select the residue where the HOLE calculation should start. This can be done by middle clicking on a residue, or by using the `Go To Atom...` dialog box.
4. Click the `Set Start Point` button in the HOLE dialog box.
5. Select the residue where the HOLE calculation should end.
6. Click the `Set End Point` button in the HOLE dialog box.
7. Click the `Calculate` button. This will generate an output file called `hole-surface-dots.dat`.
8. Run the holecmm.py script to generate a .cmm file. This example uses the colors from the .dat file. <br />
`python holecmm.py -i hole-surface-dots.dat`
9. You can also use custom colors. <br />
`python holecmm.py -i hole-surface-dots.dat -o kcsa.cmm -r 0.2 -c1 FF6347 -c2 90EE90 -c3 6495ED`
