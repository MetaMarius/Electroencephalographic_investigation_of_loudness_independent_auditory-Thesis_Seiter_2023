function cfg = razr_cfg_user
% RAZR_CFG_USER - Returns RAZR custom configuration.
% This function is intended to be edited by the user to change the default
% configuration and/or to add new configuration entries, e.g., HRTF databases
% or dry sound samples to auralize. You can also create new configuration files
% similarly to this file and store several cfg-files in parallel. To specify
% what configuration is actually used, edit the file SELECT_RAZR_CFG.M.
%
% Usage:
%   cfg = RAZR_CFG_USER
%
% See also: SELECT_RAZR_CFG, RAZR_CFG_DEFAULT


s = filesep;

%% Paths to HRTF databases and SOFA API

% Replace 'path_to' by the path to the directory where you have stored the SOFA
% API for Matlab/Octave. You can download the API from:
% https://www.sofaconventions.org/mediawiki/index.php/Software_and_APIs
%cfg.sofa_api_path = ['C:\Users\JMA\sciebo\TUB\RoomSimulations\sofaAPI', s, 'API_MO'];
%cfg.sofa_api_path = ['/Users/jakabpilaszanovich/Documents/GitHub/RoomSimulations/sofaAPI', s, 'API_MO'];
cfg.sofa_api_path = ['C:\Users\mariu\PycharmProjects\FreefieldLab\RoomSimulations\sofaAPI', s, 'API_MO'];

% Replace 'path_to_database' below by the paths to the HRTF-database locations
% on your harddrive. Fields have the format "hrtf_path__<shortcut>", where
% <shortcut> is the key associated with a certain database, e.g. cipic. It is
% used by setting the option op.hrtf_database = '<shortcut>'.
% See also EXAMPLES/EXAMPLE_HRTF.M

% Templates for some SOFA-file [0] shortcuts:
%cfg.sofa_file__fabian     = fullfile('C:\Users\JMA\sciebo\TUB\RoomSimulations\hrirs', 'FABIAN_HRIR_measured_HATO_0.sofa'); % [1]
%cfg.sofa_file__ku100      = fullfile('C:\Users\JMA\sciebo\TUB\RoomSimulations\hrirs', 'HRIR_L2702.sofa');
%cfg.sofa_file__fabian     = fullfile('/Users/jakabpilaszanovich/Documents/GitHub/RoomSimulations/hrirs', 'FABIAN_HRIR_measured_HATO_0.sofa'); % [1]
%cfg.sofa_file__ku100      = fullfile('/Users/jakabpilaszanovich/Documents/GitHub/RoomSimulations/hrirs', 'HRIR_L2702.sofa');
cfg.sofa_file__fabian     = fullfile('C:\Users\mariu\PycharmProjects\FreefieldLab\RoomSimulations/hrirs', 'FABIAN_HRIR_measured_HATO_0.sofa'); % [1]
cfg.sofa_file__ku100      = fullfile('C:\Users\mariu\PycharmProjects\FreefieldLab\RoomSimulations/hrirs', 'HRIR_L2702.sofa');
%cfg.sofa_file__cipic      = fullfile('path_to_database', 'subject_021.sofa');                 % [2]
%cfg.sofa_file__mitkemar   = fullfile('path_to_database', 'mit_kemar_normal_pinna.sofa');      % [3]
%cfg.sofa_file__mitkemar_l = fullfile('path_to_database', 'mit_kemar_large_pinna.sofa');       % [3]
%cfg.sofa_file__kayser     = fullfile('path_to_database', 'Kayser2009_Anechoic.sofa');         % [4]

% Templates for some non-SOFA database shortcuts:
%cfg.hrtf_path__cipic  = ['path_to_database', s, 'CIPIC_hrtf_database', s, 'standard_hrir_database'];        % [2]
%cfg.hrtf_path__kayser = ['path_to_database', s, 'Kayser_HRIR_Database', s, 'HRIR_database_mat', s, 'hrir']; % [4]
%cfg.hrtf_path__thiem  = ['path_to_database', s, 'HRTF_thiemann'];                                           % [5]
%cfg.hrtf_path__mk2    = ['path_to_database', s, 'TASP_MK2_Results', s 'ImpulseResponses', s, 'HRIR'];       % [6]

% References:
% [0] https://www.sofaconventions.org/
% [1] Brinkmann, F., Lindau, A., Weinzierl, S., Geissler, G., & van de Par, S.
%     (2013). A high resolution head-related transfer function database including
%     different orientations of head above the torso. In Proceedings of the
%     AIA-DAGA 2013 Conference on Acoustics.
% [2] Algazi, V. R., et al. (2001), The CIPIC HRTF Database, Proc. 2001 IEEE
%     Workshop on Applications of Signal Processing to Audio and Electroacoustics
% [3] Gardner, B. and Martin, K. (2000): HRTF Measurements of a KEMAR Dummy-Head
%     Microphone. http://sound.media.mit.edu/resources/KEMAR.html
% [4] Kayser, H., et al. (2009): Database of multichannel in-ear and behind-the-
%     ear head-related and binaural room impulse responses, EURASIP Journal on
%     Advances in Signal Processing
% [5] Thiemann, J., et al. (2015): Multiple Model High-Spatial Resolution HRTF
%     Measurements, DAGA 2015
% [6] Cortex MK2 dummy head, database measured at Uni Oldenburg, not published yet

%% Filenames (inlcuding path and extension) for sound samples used by APPLY_RIR

samples_path = [get_razr_path, s, 'base', s, 'external', s, 'samples'];
cfg.sample__uso_300ms_1 = fullfile(samples_path, 'uso_300ms_3.wav');
cfg.sample__uso_300ms_2 = fullfile(samples_path, 'uso_300ms_7.wav');
cfg.sample__uso_300ms_3 = fullfile(samples_path, 'uso_300ms_11.wav');
cfg.sample__uso_300ms_4 = fullfile(samples_path, 'uso_300ms_15.wav');
cfg.sample__uso_300ms_5 = fullfile(samples_path, 'uso_300ms_19.wav');
cfg.sample__uso_300ms_6 = fullfile(samples_path, 'uso_300ms_23.wav');
cfg.sample__uso_300ms_7 = fullfile(samples_path, 'uso_300ms_27.wav');
cfg.sample__uso_300ms_8 = fullfile(samples_path, 'uso_300ms_31.wav');
cfg.sample__uso_300ms_9 = fullfile(samples_path, 'uso_300ms_35.wav');
cfg.sample__uso_300ms_10 = fullfile(samples_path, 'uso_300ms_39.wav');
cfg.sample__uso_300ms_11 = fullfile(samples_path, 'uso_300ms_43.wav');
cfg.sample__uso_300ms_12 = fullfile(samples_path, 'uso_300ms_47.wav');
cfg.sample__uso_300ms_13 = fullfile(samples_path, 'uso_300ms_51.wav');
cfg.sample__uso_300ms_14 = fullfile(samples_path, 'uso_300ms_55.wav');
cfg.sample__uso_300ms_15 = fullfile(samples_path, 'uso_300ms_59.wav');
cfg.sample__uso_300ms_16 = fullfile(samples_path, 'uso_300ms_63.wav');
cfg.sample__uso_300ms_17 = fullfile(samples_path, 'uso_300ms_67.wav');
cfg.sample__uso_300ms_18 = fullfile(samples_path, 'uso_300ms_71.wav');
cfg.sample__uso_300ms_19 = fullfile(samples_path, 'uso_300ms_75.wav');
cfg.sample__uso_300ms_20 = fullfile(samples_path, 'uso_300ms_79.wav');
cfg.sample__uso_300ms_21 = fullfile(samples_path, 'uso_300ms_83.wav');
cfg.sample__uso_300ms_22 = fullfile(samples_path, 'uso_300ms_87.wav');
cfg.sample__uso_300ms_23 = fullfile(samples_path, 'uso_300ms_91.wav');
cfg.sample__uso_300ms_24 = fullfile(samples_path, 'uso_300ms_95.wav');
cfg.sample__uso_300ms_25 = fullfile(samples_path, 'uso_300ms_99.wav');
cfg.sample__uso_300ms_26 = fullfile(samples_path, 'uso_300ms_103.wav');
cfg.sample__uso_300ms_27 = fullfile(samples_path, 'uso_300ms_107.wav');
cfg.sample__uso_300ms_28 = fullfile(samples_path, 'uso_300ms_111.wav');
cfg.sample__uso_300ms_29 = fullfile(samples_path, 'uso_300ms_115.wav');
cfg.sample__uso_300ms_30 = fullfile(samples_path, 'uso_300ms_119.wav');


%% Headphone equalization files
% Fieldnames must have the following format:
% hp_eq__<headphone_key>_<samplingrate>

cfg.hp_eq__hd650_44100 = fullfile(get_razr_path, 'analysis_tools', 'headphone_eq', 'hd650_44k.mat');
cfg.hp_eq__hd650_48000 = fullfile(get_razr_path, 'analysis_tools', 'headphone_eq', 'hd650_48k.mat');

% Key string for default headphone equalization (used by APPLY_RIR):
cfg.default_headphone = 'none';  % supported up to now: 'none', 'hd650'
