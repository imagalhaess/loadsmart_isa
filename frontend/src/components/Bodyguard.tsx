/**
 * Bodyguard Component - Easter Egg Feature
 * Fun interactive feature to choose a personal bodyguard.
 */
import { useState } from 'react';
import JorgeImg from '../assets/jorge.jpg';
import JoséImg from '../assets/jose.jpg';
import MaitêImg from '../assets/maite.jpg';

type BodyguardName = 'Jorge' | 'Maitê' | 'José';

interface Bodyguard {
  name: BodyguardName;
  image: string;
}

const bodyguards: Record<BodyguardName, Bodyguard> = {
  Jorge: { name: 'Jorge', image: JorgeImg },
  Maitê: { name: 'Maitê', image: MaitêImg },
  José: { name: 'José', image: JoséImg },
};

export const Bodyguard = () => {
  const [selectedBodyguard, setSelectedBodyguard] = useState<BodyguardName | ''>('');
  const [confirmedBodyguard, setConfirmedBodyguard] = useState<Bodyguard | null>(null);

  const handleConfirm = () => {
    if (selectedBodyguard) {
      setConfirmedBodyguard(bodyguards[selectedBodyguard]);
    }
  };

  const handleReset = () => {
    setSelectedBodyguard('');
    setConfirmedBodyguard(null);
  };

  return (
    <div className="bodyguard-container">
      {!confirmedBodyguard ? (
        <div className="bodyguard-selection">
          <h2>Choose a Bodyguard to Protect You From All Evils</h2>
          <p className="bodyguard-description">
            Select your personal bodyguard who will keep you safe from all dangers.
          </p>

          <div className="form-group">
            <label htmlFor="bodyguard-select">Select Your Protector:</label>
            <select
              id="bodyguard-select"
              className="form-control"
              value={selectedBodyguard}
              onChange={(e) => setSelectedBodyguard(e.target.value as BodyguardName)}
            >
              <option value="">-- Choose Wisely --</option>
              <option value="Jorge">Jorge</option>
              <option value="Maitê">Maitê</option>
              <option value="José">José</option>
            </select>
          </div>

          <button
            className="btn btn-primary"
            onClick={handleConfirm}
            disabled={!selectedBodyguard}
            style={{ marginTop: '1rem' }}
          >
            Confirm Selection
          </button>
        </div>
      ) : (
        <div className="bodyguard-confirmed">
          <h2>{confirmedBodyguard.name} Will Protect You From Now On!</h2>
          <p className="bodyguard-message">
            You are now under the protection of {confirmedBodyguard.name}. Sleep well knowing you're safe!
          </p>

          <div className="bodyguard-image-container">
            <img
              src={confirmedBodyguard.image}
              alt={`${confirmedBodyguard.name} - Your Bodyguard`}
              className="bodyguard-image"
            />
          </div>

          <button
            className="btn btn-secondary"
            onClick={handleReset}
            style={{ marginTop: '1.5rem' }}
          >
            Choose Another Bodyguard
          </button>
        </div>
      )}
    </div>
  );
};
