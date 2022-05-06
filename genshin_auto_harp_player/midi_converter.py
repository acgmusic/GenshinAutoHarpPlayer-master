from collections import Counter
import pretty_midi

# 调内音模12余数
KEY_C_MOD = [0, 2, 4, 5, 7, 9, 11]
# 转换离调音
CHANGE_MAP = {1: -4, 3: -4, 6: -4, 8: -4, 10: -8}


def isPlayableMidi(load_fp):
    pass


def midi_converter(load_fp, save_fp=None):
    midi_data = pretty_midi.PrettyMIDI(midi_file=load_fp)
    midi_data_new = pretty_midi.pretty_midi.PrettyMIDI()
    midi_data_new.instruments = [pretty_midi.instrument.Instrument(program=2)]

    for inst in midi_data.instruments:
        if not inst.is_drum:
            midi_data_new.instruments[0].notes += inst.notes

    notes = midi_data_new.instruments[0].notes
    notes.sort(key=lambda x: x.start)

    notes_remove_dup = []
    pitch_set = set()

    for i in range(len(notes)):
        if i == 0 or (notes[i].start != notes_remove_dup[-1].start):
            notes_remove_dup.append(notes[i])
            pitch_set = {notes[i].pitch}
        elif notes[i].pitch not in pitch_set:
            pitch_set.add(notes[i].pitch)
            notes_remove_dup.append(notes[i])

    # 先确定最合理的调性
    score_pitch = [sum([(note.pitch + i) % 12 in KEY_C_MOD for note in notes]) / len(notes) for i in range(12)]
    up_pitch = score_pitch.index(max(score_pitch))

    # 确定3个八度合理的范围
    score_octave = [sum([36 <= (note.pitch + up_pitch + 12 * i) <= 71 for note in notes]) / len(notes) for i in
                    range(-9, 10)]
    up_octave_index = score_octave.index(max(score_octave))
    up_octave = list(range(-9, 10))[up_octave_index]
    up_pitch_final = up_pitch + 12 * up_octave

    # 处理离调音
    for note in notes:
        note.pitch += up_pitch_final
        note.pitch += CHANGE_MAP.get(note.pitch % 12, 0)
        while note.pitch < 36:
            note.pitch += 12
        while note.pitch > 71:
            note.pitch -= 12

    # 去除开头结尾的多余空白
    # 去除中间的空白
    total_intv = [notes[i + 1].start - notes[i].start for i in range(len(notes) - 1)]
    counter = Counter(total_intv).most_common(2)
    start_new = 8 * counter[0][0] if counter[0][0] or len(counter) == 1 else counter[1][0]
    _trans_time(notes, start_new, 0, len(notes))

    for i in range(1, len(notes)):
        if notes[i].start - notes[i - 1].start > start_new * 32:
            _trans_time(notes, notes[i - 1].start + start_new * 16, i, len(notes))
    # fp_new = fp.split('.')[0] + "(modified)." + fp.split('.')[-1]
    if save_fp:
        midi_data_new.write(save_fp)
    return midi_data_new


def _trans_time(notes, start_new, pos_from, pos_to):
    diff = notes[pos_from].start - start_new
    for i in range(pos_from, pos_to):
        notes[i].start -= diff
        notes[i].end -= diff


