import { RouterProvider } from '@tanstack/react-router';
import { useEffect } from 'react';

import { getBaseUrl } from '@lib/functions/Navigation';
import { useShallow } from 'zustand/react/shallow';
import { api, queryClient } from '../App';
import { ApiProvider } from '../contexts/ApiContext';
import { ThemeContext } from '../contexts/ThemeContext';
import { defaultHostList } from '../defaults/defaultHostList';
import { router } from '../router';
import { useLocalState } from '../states/LocalState';

export default function DesktopAppView() {
  const [hostList] = useLocalState(useShallow((state) => [state.hostList]));

  useEffect(() => {
    if (Object.keys(hostList).length === 0) {
      useLocalState.setState({ hostList: defaultHostList });
    }
  }, [hostList]);

  // Set the basepath for the router
  const basepath = getBaseUrl();

  return (
    <ApiProvider client={queryClient} api={api}>
      <ThemeContext>
        <RouterProvider router={router} basepath={basepath} />
      </ThemeContext>
    </ApiProvider>
  );
}
