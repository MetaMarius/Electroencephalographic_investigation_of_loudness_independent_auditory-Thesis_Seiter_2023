% Example script for defining and auralizing different source distances. 
% Two source distances in two rooms are simulated and automatically played 
% back. 


%% Please see EXAMPLE_DEFAULT first for a demonstration of the basic concepts of RAZR.
%%
clear;
clear global;
cfg = select_razr_cfg;

filename_list = [
  "uso_300ms_1"
  "uso_300ms_2"
  "uso_300ms_3"
  "uso_300ms_4"
  "uso_300ms_5"
  "uso_300ms_6"
  "uso_300ms_7"
  "uso_300ms_8"
  "uso_300ms_9"
  "uso_300ms_10"
  "uso_300ms_11"
  "uso_300ms_12"
  "uso_300ms_13"
  "uso_300ms_14"
  "uso_300ms_15"
  "uso_300ms_16"
  "uso_300ms_17"
  "uso_300ms_18"
  "uso_300ms_19"
  "uso_300ms_20"
  "uso_300ms_21"
  "uso_300ms_22"
  "uso_300ms_23"
  "uso_300ms_24"
  "uso_300ms_25"
  "uso_300ms_26"
  "uso_300ms_27"
  "uso_300ms_28"
  "uso_300ms_29"
  "uso_300ms_30"
    ];

% distances = [0, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 12.8];
% distances = 0: 0.2: 20;
distances = [0.18, 0.19, 0.2, 0.21, 0.22,...
             1.62, 1.71, 1.8, 1.89, 1.98,...
             4.5, 4.75, 5, 5.25, 5.5,...
             10.8, 11.4, 12, 12.6, 13.2,... 
             22.5, 23.75, 25, 26.25, 27.5];
%y = logspace(log10(0.2), log10(25), 5);
%distances = [0.17,	0.18,	0.19,	0.20,	0.21,	0.22,	0.23...
 %            0.57,	0.60,	0.64,	0.67,	0.70,	0.74,	0.77...
  %           1.90,	2.01,   2.12,	2.24,	2.35,	2.46,	2.57...
   %          6.36,	6.73,	7.10,	7.48,	7.85,	8.22,	8.60...
    %         21.25,	22.50,	23.75,	25.00,	26.25,	27.50,	28.75];



size_x = 10;
size_y = 35;
size_z = 3;

recpos_x = size_x/2;
recpos_y = 3.0;
recpos_z = 1.5;

filename_room = "_room-" + num2str(size_x) + "-" + num2str(size_y) + "-" + num2str(size_z);

for i = 1:length(filename_list)
    
    filename_core = filename_list(i);

    % Load example room L:
    room = get_room_A;
    room.boxsize   = [size_x, size_y, size_z];

    % Setup of source and receiver, distance 2.5 m
    room.recpos = [recpos_x, recpos_y , recpos_z];

    out_root_folder_name = filename_core + filename_room;
    out_root_folder_path = "C:\Users\mariu\PycharmProjects\FreefieldLab\USOgen\data\distance_simulation\final_distances\" + out_root_folder_name;
    %out_simulated_folder_path = out_root_folder_path + "/simulated";

    if ~exist(out_root_folder_path, 'dir')
       mkdir(out_root_folder_path)
    end

    for distance = distances
        if distance == 0
            room.materials = [0.99, 0.99, 0.99, 0.99, 0.99];
            room.srcpos = [recpos_x, recpos_y + 0.05, recpos_z];
            filename_full = filename_core + filename_room + "_control.wav";
        else
            room.materials = [0.05, 0.1, 0.13, 0.16, 0.22];
            room.recdir	= [90, 0];
            room.srcpos = [recpos_x, recpos_y + distance, recpos_z];
            filename_full = filename_core + filename_room + "_dist-" + num2str(distance * 100) + ".wav";
        end
        ir = razr(room);
        out = apply_rir(ir, 'src', filename_core);

        out_filename_path = out_root_folder_path + "/" + filename_full;
        audiowrite(out_filename_path, out{1}, ir.fs);
        disp("writing: " + filename_full);
    end

    disp("done");
end