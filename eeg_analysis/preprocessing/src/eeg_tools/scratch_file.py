import mne.epochs

if "filtering" in config:
    raw = filtering(data=raw, **config["filtering"])
if "epochs" in config:
    events= mne.events_from_annotations(raw)[0]
    print('Starting creation of metadata')  # processed
    metadata = create_metadata(raw=raw, root_path=root_path, id=id)
    print('Metadata  creation finished')
    print('Create epochs with attached metadata')
    epochs = mne.Epochs(raw, events=events, metadata=metadata,
                        **config["epochs"], preload=True)     # include all event ids in event id dictionary!!
    epochs = shift_epochs_by_onset_delay()
    epochs.crop(tmin=tmin, tmax=tmax, include_tmax=True)
    epochs.plot(show=False, show_scalebars=False,
                show_scrollbars=False, n_channels=20)
    plt.savefig(_fig_folder / pathlib.Path("epochs.jpg"), dpi=800)
    plt.close()





first_epochs = mne.epochs.read_epochs(fname='C:/Users/ms26cize/USO_Bachelor_Thesis/updated_analysis/data/1r3qdv/epochs/1r3qdv-epo.fif')