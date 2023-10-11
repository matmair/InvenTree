import { QueryClientProvider } from '@tanstack/react-query';
import { useEffect, useState } from 'react';
import { BrowserRouter } from 'react-router-dom';

import { queryClient, setApiDefaults } from '../App';
import { BaseContext } from '../contexts/BaseContext';
import { defaultHostList } from '../defaults/defaultHostList';
import { url_base } from '../main';
import { routes } from '../router';
import { useLocalState } from '../states/LocalState';
import { useSessionState } from '../states/SessionState';
import {
  useGlobalSettingsState,
  useUserSettingsState
} from '../states/SettingsState';
import { useUserState } from '../states/UserState';

export default function DesktopAppView() {
  const [hostList] = useLocalState((state) => [state.hostList]);
  const [fetchUserState] = useUserState((state) => [state.fetchUserState]);

  const [fetchGlobalSettings] = useGlobalSettingsState((state) => [
    state.fetchSettings
  ]);
  const [fetchUserSettings] = useUserSettingsState((state) => [
    state.fetchSettings
  ]);

  // Local state initialization
  if (Object.keys(hostList).length === 0) {
    console.log('Loading default host list');
    useLocalState.setState({ hostList: defaultHostList });
  }
  setApiDefaults();

  // Server Session
  const [fetchedServerSession, setFetchedServerSession] = useState(false);
  const sessionState = useSessionState.getState();
  const [token] = sessionState.token ? [sessionState.token] : [null];
  useEffect(() => {
    if (token && !fetchedServerSession) {
      setFetchedServerSession(true);
      fetchUserState();
      fetchGlobalSettings();
      fetchUserSettings();
    }
  }, [token, fetchedServerSession]);

  return (
    <BaseContext>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter basename={url_base}>{routes}</BrowserRouter>
      </QueryClientProvider>
    </BaseContext>
  );
}
